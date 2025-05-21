import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.cats import CatSchema


class TargetCreateSchema(BaseModel):
    name: str
    country: str


class TargetSchema(TargetCreateSchema):
    id: uuid.UUID
    notes: Optional[str] = None
    is_completed: bool
    created_at: datetime
    updated_at: datetime


class TargetUpdateSchema(BaseModel):
    notes: Optional[str] = None
    is_completed: Optional[bool] = None


class MissionCreateSchema(BaseModel):
    cat_id: uuid.UUID
    targets: list[TargetCreateSchema]


class MissionSchema(BaseModel):
    id: uuid.UUID
    targets: list[TargetSchema]
    cat: CatSchema
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MissionUpdateSchema(BaseModel):
    is_completed: Optional[bool] = None
    cat_id: Optional[uuid.UUID] = None
