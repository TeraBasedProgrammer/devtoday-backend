import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies.services import get_cats_service
from app.schemas.cats import CatCreateSchema, CatSchema, CatUpdateSchema
from app.services.cats import CatService

router = APIRouter(prefix="/cats", tags=["Cats"])


@router.get("/")
async def get_cats(
    cats_service: Annotated[CatService, Depends(get_cats_service)],
) -> list[CatSchema]:
    return await cats_service.get_cats()


@router.get("/{cat_id}")
async def get_cat(
    cat_id: uuid.UUID,
    cats_service: Annotated[CatService, Depends(get_cats_service)],
) -> CatSchema:
    return await cats_service.get_cat(cat_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_cat(
    cat_data: CatCreateSchema,
    cats_service: Annotated[CatService, Depends(get_cats_service)],
) -> CatSchema:
    return await cats_service.create_cat(cat_data)


@router.patch("/{cat_id}")
async def update_cat(
    cat_id: uuid.UUID,
    cat_data: CatUpdateSchema,
    cats_service: Annotated[CatService, Depends(get_cats_service)],
) -> CatSchema:
    return await cats_service.update_cat(cat_id, cat_data)


@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cat(
    cat_id: uuid.UUID,
    cats_service: Annotated[CatService, Depends(get_cats_service)],
) -> None:
    return await cats_service.delete_cat(cat_id)
