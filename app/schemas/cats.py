import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CatCreateSchema(BaseModel):
    name: str
    breed: str
    experience: int
    salary: int


class CatSchema(CatCreateSchema):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CatUpdateSchema(BaseModel):
    salary: Optional[int] = None
