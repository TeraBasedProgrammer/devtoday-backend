from fastapi import APIRouter

from app.api.routes.cats import router as cats_router
from app.api.routes.missions import router as missions_router

router = APIRouter()

router.include_router(cats_router)
router.include_router(missions_router)
