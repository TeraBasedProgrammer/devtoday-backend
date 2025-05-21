import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CatCreateSchema(BaseModel):
    name: str = Field(..., max_length=100)
    breed: str = Field(..., max_length=100)
    experience: int = Field(..., gt=0)
    salary: int = Field(..., gt=0)


class CatSchema(CatCreateSchema):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CatUpdateSchema(BaseModel):
    salary: Optional[int] = Field(None, gt=0)
