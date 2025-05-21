from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.session import get_async_session
from app.services.cats import CatService
from app.services.missions import MissionService


def get_cats_service(session: AsyncSession = Depends(get_async_session)) -> CatService:
    return CatService(session)


def get_missions_service(
    session: AsyncSession = Depends(get_async_session),
) -> MissionService:
    return MissionService(session)
