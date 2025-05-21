import uuid
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.config.logs.logger import logger
from app.models.cats import Cat
from app.models.missions import Mission, Target
from app.schemas.missions import (
    MissionCreateSchema,
    MissionSchema,
    MissionUpdateSchema,
    TargetCreateSchema,
    TargetSchema,
    TargetUpdateSchema,
)
from app.services.base import BaseService


class MissionService(BaseService):
    model = Mission

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_missions(self) -> list[MissionSchema]:
        logger.info("Getting all missions")
        missions_data = await self.get_all(
            select(Mission).options(
                joinedload(Mission.cat), joinedload(Mission.targets)
            )
        )
        return [MissionSchema.from_instance(mission) for mission in missions_data]

    async def get_mission(self, mission_id: uuid.UUID) -> MissionSchema:
        logger.info("Getting a mission by id")
        mission = await self.get_instance(
            select(Mission)
            .where(Mission.id == mission_id)
            .options(joinedload(Mission.cat), joinedload(Mission.targets))
        )
        return MissionSchema.from_instance(mission)

    async def create_mission(self, mission_data: MissionCreateSchema) -> None:
        logger.info("Creating a mission")
        mission_targets: list[TargetCreateSchema] = mission_data.targets
        if len(mission_targets) > 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mission targets quantity must be from 1 to 3",
            )

        mission_data.targets = []
        mission: Mission = await self.create(mission_data)

        logger.info("Creating targets for a mission")
        for target in mission_targets:
            target.mission_id = mission.id
            await self.create(target, Target)

    async def update_mission(
        self, mission_id: uuid.UUID, mission_data: MissionUpdateSchema
    ) -> MissionSchema:
        logger.info("Updating a mission")
        mission: Optional[Mission] = await self.get_instance(
            select(Mission)
            .where(Mission.id == mission_id)
            .options(joinedload(Mission.targets))
        )
        if not mission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found"
            )

        logger.info("Checking if the mission is already completed")
        if mission.is_completed and mission_data.is_completed is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mission already completed",
            )

        logger.info("Checking if the cat is already assigned to the mission")
        if mission_data.cat_id:
            if mission.cat_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Mission cat already assigned",
                )
            cat = await self.get_instance(
                select(Cat).where(Cat.id == mission_data.cat_id)
            )
            if not cat:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found"
                )

        logger.info("Updating the mission targets in case of completion")
        if mission_data.is_completed:
            for target in mission.targets:
                target.is_completed = True
                await self.save(target)

        await self.update(mission_id, mission_data)
        refreshed_mission = await self.get_instance(
            select(Mission)
            .where(Mission.id == mission_id)
            .options(joinedload(Mission.cat), joinedload(Mission.targets))
        )
        return MissionSchema.from_instance(refreshed_mission)

    async def delete_mission(self, mission_id: uuid.UUID) -> None:
        logger.info("Deleting a mission")
        mission: Optional[Mission] = await self.get_instance(
            select(Mission).where(Mission.id == mission_id)
        )
        if not mission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found"
            )

        if mission.cat_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mission cat already assigned",
            )

        await self.delete(mission_id)

    async def update_target(
        self, target_id: uuid.UUID, target_data: TargetUpdateSchema
    ) -> TargetSchema:
        logger.info("Updating a target")
        target: Optional[Target] = await self.get_instance(
            select(Target).where(Target.id == target_id)
        )

        if not target:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Target not found"
            )

        logger.info("Checking if the target is already completed")
        if target.is_completed and (
            target_data.is_completed is not None or target_data.notes
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Target already completed",
            )

        refreshed_target = await self.update(target_id, target_data, Target)
        return TargetSchema(**refreshed_target.__dict__)
