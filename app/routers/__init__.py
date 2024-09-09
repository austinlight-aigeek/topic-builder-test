from fastapi import APIRouter
from app.routers.app import router as app_router

router = APIRouter()

router.include_router(
    app_router,
)
