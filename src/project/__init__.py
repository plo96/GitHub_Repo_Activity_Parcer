"""
	Общие файлы для проектаЖ
	- Конфиги приложения;
	- Кастомные декораторы;
	- Кастомные исключения.
"""
__all__ = (
	"settings",
	"exceptions",
	"decorators",
)

from .config import settings
from . import exceptions
from . import decorators
