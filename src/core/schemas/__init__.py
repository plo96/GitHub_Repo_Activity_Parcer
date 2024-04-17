"""
	Модуль, содержащий pydantic-схемы для сущностей
"""
__all__ = (
	"RepoDTO",
	"RepoActivityDTO",
)
from .repos import RepoDTO
from .repo_activities import RepoActivityDTO
