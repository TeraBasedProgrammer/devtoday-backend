import uuid
from typing import Optional

import httpx
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.config.logs.logger import logger
from app.models.cats import Cat
from app.schemas.cats import CatCreateSchema, CatSchema, CatUpdateSchema
from app.services.base import BaseService


class CatService(BaseService):
    model = Cat

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_cats(self) -> list[CatSchema]:
        logger.info("Getting all cats")
        cats_data = await self.get_all(select(Cat))
        return [CatSchema(**cat.__dict__) for cat in cats_data]

    async def get_cat(self, cat_id: uuid.UUID) -> CatSchema:
        logger.info("Getting a cat by id")
        cat_instance: Optional[Cat] = await self.get_instance(
            select(Cat).where(Cat.id == cat_id)
        )
        if not cat_instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cat not found",
            )
        return CatSchema(**cat_instance.__dict__)

    async def create_cat(self, cat_data: CatCreateSchema) -> CatSchema:
        logger.info("Creating a new cat")

        logger.info("Validating the cat's breed")

        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.thecatapi.com/v1/breeds")
            existing_breeds = [breed["name"] for breed in response.json()]
            if cat_data.breed not in existing_breeds:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid breed provided",
                )

        new_cat = await self.create(cat_data)
        return CatSchema(**new_cat.__dict__)

    async def update_cat(
        self, cat_id: uuid.UUID, cat_data: CatUpdateSchema
    ) -> CatSchema:
        logger.info("Updating a cat")
        cat_instance = await self.get_instance(select(Cat).where(Cat.id == cat_id))
        if not cat_instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cat not found",
            )

        updated_cat = await self.update(cat_id, cat_data)
        return CatSchema(**updated_cat.__dict__)

    async def delete_cat(self, cat_id: uuid.UUID) -> None:
        logger.info("Deleting a cat")
        cat_data: Optional[Cat] = await self.get_instance(
            select(Cat).where(Cat.id == cat_id).options(joinedload(Cat.missions))
        )
        if not cat_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cat not found",
            )

        if cat_data.missions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can't delete cat with missions",
            )

        await self.delete(cat_id)
