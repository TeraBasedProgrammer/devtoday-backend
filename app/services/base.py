from itertools import chain
from typing import Any, Iterable, Optional, Type

from pydantic import BaseModel
from sqlalchemy import Select, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base


class BaseService:
    model: Optional[Type[Base]] = None

    def __init__(self, session: AsyncSession):
        self.session = session

    def unpack(self, collection: Iterable) -> list:
        return list(chain.from_iterable(collection))

    async def get_all(self, query: Select) -> list[Any]:
        response = await self.session.execute(query)
        result = self.unpack(response.unique().all())
        return result

    async def create(
        self, model_data: Type[BaseModel], model: Type[Base] = None
    ) -> Type[Base]:
        model_instance = model or self.model
        new_instance = model_instance(**model_data.model_dump())
        self.session.add(new_instance)

        await self.session.commit()
        return new_instance

    async def get_instance(self, query: Select) -> Optional[Base]:
        response = await self.session.execute(query)
        result = response.unique().scalar_one_or_none()
        return result

    async def update(
        self, instance_id: int, model_data: Type[BaseModel], model: Type[Base] = None
    ) -> Type[Base]:
        model_instance = model or self.model
        query = (
            update(model_instance)
            .where(model_instance.id == instance_id)
            .values(
                {
                    key: value
                    for key, value in model_data.model_dump().items()
                    if value is not None
                }
            )
            .returning(model_instance)
        )
        res = await self.session.execute(query)
        await self.session.commit()
        return res.unique().scalar_one()

    async def delete(self, instance_id: int) -> int:
        query = (
            delete(self.model)
            .where(self.model.id == instance_id)
            .returning(self.model.id)
        )

        result = (await self.session.execute(query)).scalar_one()
        await self.session.commit()
        return result

    async def save(self, obj: Any):
        self.session.add(obj)
        await self.session.commit()

    async def save_many(self, objects: list[Any], with_expire: bool = False):
        self.session.add_all(objects)
        await self.session.commit()
        if with_expire:
            self.session.expire_all()
