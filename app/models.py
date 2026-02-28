from pydantic import BaseModel, field_validator


class InquiryRequest(BaseModel):
    text: str
    language: str = "no"

    @field_validator("text")
    @classmethod
    def text_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("text must not be empty")
        return v


class InquiryResponse(BaseModel):
    category: str
    summary: str
    suggested_action: str
    confidence: float
    processing_time_ms: float


class HealthResponse(BaseModel):
    status: str
    version: str
