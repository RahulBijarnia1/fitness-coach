from pydantic import BaseModel, Field
from typing import Optional


class ProfileCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=13, le=120)
    sex: str = Field(..., pattern=r"^(male|female)$")
    height: float = Field(..., gt=0, le=300)   # cm
    weight: float = Field(..., gt=0, le=500)   # kg
    body_fat: Optional[float] = Field(None, ge=1, le=60)  # percentage


class ProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=13, le=120)
    sex: Optional[str] = Field(None, pattern=r"^(male|female)$")
    height: Optional[float] = Field(None, gt=0, le=300)
    weight: Optional[float] = Field(None, gt=0, le=500)
    body_fat: Optional[float] = Field(None, ge=1, le=60)


class ProfileOut(BaseModel):
    id: int
    user_id: int
    name: str
    age: int
    sex: str
    height: float
    weight: float
    body_fat: Optional[float]

    model_config = {"from_attributes": True}


# Alias for API v1 endpoints
ProfileResponse = ProfileOut
