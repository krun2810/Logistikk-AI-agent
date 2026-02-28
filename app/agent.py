from __future__ import annotations

import json
import re
import time
from typing import Any

from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from app.models import InquiryRequest, InquiryResponse
from app.tools import categorize_by_keywords, extract_tracking_number

# Type alias for the compiled LangGraph agent
Agent = Any


@tool
def categorize_inquiry(text: str) -> str:
    """Categorize a logistics inquiry into one of: pakke_sporing, klage, adresse_endring, generell_henvendelse"""
    return categorize_by_keywords(text)


@tool
def get_tracking_info(text: str) -> str:
    """Extract and return tracking number from inquiry text"""
    number = extract_tracking_number(text)
    return f"Tracking number found: {number}" if number else "No tracking number found"


SYSTEM_PROMPT = """You are an AI logistics assistant for a Norwegian shipping company.
Your job is to help process customer inquiries by:
1. Categorizing the inquiry type
2. Summarizing the key information
3. Suggesting an appropriate action or response

Always respond in JSON format with fields: category, summary, suggested_action, confidence (0.0-1.0)
Be concise and professional."""


def create_agent() -> Agent:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [categorize_inquiry, get_tracking_info]
    return create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)


def process_inquiry(
    request: InquiryRequest, agent: Agent | None = None
) -> InquiryResponse:
    if agent is None:
        agent = create_agent()
    start = time.time()

    # Try agentops tracking if available
    try:
        import agentops

        session = agentops.start_session(tags=["logistics", "inquiry"])
    except Exception:
        session = None

    try:
        result = agent.invoke({"messages": [("human", request.text)]})
        # langgraph returns messages list; extract last AI message content
        messages = result.get("messages", [])
        output = messages[-1].content if messages else ""
        json_match = re.search(r"\{.*\}", output, re.DOTALL)
        if json_match:
            data: dict[str, Any] = json.loads(json_match.group())
        else:
            category = categorize_by_keywords(request.text)
            data = {
                "category": category,
                "summary": output[:200],
                "suggested_action": "Forward to appropriate department",
                "confidence": 0.6,
            }
    except Exception as e:
        category = categorize_by_keywords(request.text)
        data = {
            "category": category,
            "summary": f"Could not fully process: {str(e)[:100]}",
            "suggested_action": "Manual review required",
            "confidence": 0.3,
        }
    finally:
        if session:
            try:
                agentops.end_session("Success")
            except Exception:
                pass

    elapsed_ms = (time.time() - start) * 1000
    return InquiryResponse(
        category=data.get("category", "generell_henvendelse"),
        summary=data.get("summary", ""),
        suggested_action=data.get("suggested_action", ""),
        confidence=float(data.get("confidence", 0.5)),
        processing_time_ms=round(elapsed_ms, 2),
    )
