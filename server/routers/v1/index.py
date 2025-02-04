from fastapi import APIRouter
from . import admin_router, user_router


router = APIRouter(prefix="/api/v1")


router.include_router(admin_router.router)
router.include_router(user_router.router)