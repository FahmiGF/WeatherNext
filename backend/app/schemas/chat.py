"""Chat-related Pydantic schemas."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=64)
    message: str = Field(min_length=1, max_length=2000)
    location: Optional[str] = None


class ChatMessageOut(BaseModel):
    role: str
    content: str
    function_calls: Optional[dict[str, Any]] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatResponseData(BaseModel):
    session_id: str
    reply: str
    intent: Optional[str] = None
    weather_data: Optional[dict[str, Any]] = None
    suggestions: list[str] = Field(default_factory=list)


class ChatSessionOut(BaseModel):
    session_id: str
    created_at: datetime
    last_message_at: datetime
    message_count: int
    location_context: Optional[str] = None

    model_config = {"from_attributes": True}
