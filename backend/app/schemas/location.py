"""Location-related Pydantic schemas."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class LocationBase(BaseModel):
    city: str
    province: str
    country: str = "Indonesia"
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    timezone: str = "Asia/Jakarta"
    bmkg_code: Optional[str] = None


class LocationCreate(LocationBase):
    pass


class LocationOut(LocationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class LocationSearch(BaseModel):
    """Query parameters for location search."""
    q: str = Field(min_length=1, description="Search query")
