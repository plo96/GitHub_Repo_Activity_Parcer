"""
    Модуль с реализацией роутеров для взаимодействия с приложением по API.
"""
__all__ = (
    "router",
)

from fastapi import APIRouter

from .repos import router as repos_router
from .repo_activities import router as repo_activities_router

router = APIRouter()

router.include_router(repos_router)
router.include_router(repo_activities_router)
