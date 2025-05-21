import uuid
from datetime import datetime
from typing import Optional, Self

from pydantic import BaseModel

from app.models.missions import Mission
from app.schemas.cats import CatSchema


class TargetCreateSchema(BaseModel):
    name: str
    country: str
    mission_id: Optional[uuid.UUID] = None


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
    targets: list[TargetCreateSchema]


class MissionSchema(BaseModel):
    id: uuid.UUID
    targets: list[TargetSchema]
    cat: Optional[CatSchema] = None
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_instance(cls, obj: Mission) -> Self:
        return cls(
            id=obj.id,
            targets=[TargetSchema(**target.__dict__) for target in obj.targets],
            cat=CatSchema(**obj.cat.__dict__) if obj.cat else None,
            is_completed=obj.is_completed,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )


class MissionUpdateSchema(BaseModel):
    is_completed: Optional[bool] = None
    cat_id: Optional[uuid.UUID] = None
