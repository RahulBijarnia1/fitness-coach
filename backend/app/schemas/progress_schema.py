from datetime import date
from pydantic import BaseModel, Field
from typing import Optional


class ProgressLogCreate(BaseModel):
    weight: float = Field(..., gt=0, le=500)
    body_fat: Optional[float] = Field(None, ge=1, le=60)
    date: Optional[date] = None


# Alias for API v1 endpoints
ProgressCreate = ProgressLogCreate


class ProgressLogOut(BaseModel):
    id: int
    user_id: int
    weight: float
    body_fat: Optional[float]
    date: date

    model_config = {"from_attributes": True}


class ProgressHistoryResponse(BaseModel):
    logs: list[ProgressLogOut]
    total: int
    page: int
    page_size: int
