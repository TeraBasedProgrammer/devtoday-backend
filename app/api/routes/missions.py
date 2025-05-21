import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies.services import get_missions_service
from app.schemas.missions import (
    MissionCreateSchema,
    MissionSchema,
    MissionUpdateSchema,
    TargetSchema,
    TargetUpdateSchema,
)
from app.services.missions import MissionService

router = APIRouter(prefix="/missions", tags=["Missions"])


@router.get("/")
async def get_missions(
    missions_service: Annotated[MissionService, Depends(get_missions_service)],
) -> list[MissionSchema]:
    return await missions_service.get_missions()


@router.get("/{mission_id}")
async def get_mission(
    mission_id: uuid.UUID,
    missions_service: Annotated[MissionService, Depends(get_missions_service)],
) -> MissionSchema:
    return await missions_service.get_mission(mission_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_mission(
    mission_data: MissionCreateSchema,
    missions_service: Annotated[MissionService, Depends(get_missions_service)],
) -> None:
    await missions_service.create_mission(mission_data)


@router.patch("/{mission_id}")
async def update_mission(
    mission_id: uuid.UUID,
    mission_data: MissionUpdateSchema,
    missions_service: Annotated[MissionService, Depends(get_missions_service)],
) -> MissionSchema:
    return await missions_service.update_mission(mission_id, mission_data)


@router.delete("/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mission(
    mission_id: uuid.UUID,
    missions_service: Annotated[MissionService, Depends(get_missions_service)],
) -> None:
    return await missions_service.delete_mission(mission_id)


@router.patch("/mission/target/{target_id}")
async def update_target(
    target_id: uuid.UUID,
    target_data: TargetUpdateSchema,
    missions_service: Annotated[MissionService, Depends(get_missions_service)],
) -> TargetSchema:
    return await missions_service.update_target(target_id, target_data)
