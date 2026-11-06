"""Common response wrappers and shared schemas."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class MetaInfo(BaseModel):
    """Metadata attached to every API response."""
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source: str = "weathernext-ai"
    disclaimer: str = (
        "Prakiraan AI ini adalah estimasi dan tidak menggantikan "
        "peringatan resmi BMKG."
    )


class APIResponse(BaseModel, Generic[T]):
    """Standard envelope for all API responses."""
    success: bool = True
    data: T
    meta: MetaInfo = Field(default_factory=MetaInfo)


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail
    meta: MetaInfo = Field(default_factory=MetaInfo)
