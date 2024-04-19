"""
    Модуль с описанием возможностей взаимодействия с БД для различных сущностей
"""
__all__ = (
    "ReposRepository",
    "RepoActivitiesRepository",
)

from .repos import ReposRepository
from .repo_activities import RepoActivitiesRepository
