"""
    Модуль с реализацией конкретных роутеров для различных сущностей
"""
__all__ = (
    "router",
)

from fastapi import APIRouter

from .repos import router as repos_router

router = APIRouter(tags=['api_v1'])

router.include_router(repos_router)
