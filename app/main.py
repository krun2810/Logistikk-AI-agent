from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.agent import create_agent, process_inquiry
from app.models import HealthResponse, InquiryRequest, InquiryResponse

VERSION = "1.0.0"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    if os.getenv("OPENAI_API_KEY"):
        app.state.agent = create_agent()
    else:
        app.state.agent = None
    yield


app = FastAPI(title="Logistikk AI-Agent", version=VERSION, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", version=VERSION)


@app.post("/inquiries", response_model=InquiryResponse)
def handle_inquiry(request: InquiryRequest) -> InquiryResponse:
    return process_inquiry(request, agent=getattr(app.state, "agent", None))
