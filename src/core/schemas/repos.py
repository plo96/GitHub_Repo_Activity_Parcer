"""
	Схемы для работы с сущностями репозиториев GitHub.
"""
from typing import Optional

from pydantic import BaseModel


class RepoBase(BaseModel):
	"""Базовый класс для репозиториев GH"""
	pass


class RepoParsing(RepoBase):
	"""Результат парсинга для репозиториев GH"""
	repo: str  # full_name репозитория
	owner: str  # Владелец репозитория
	position_cur: int  # Текущая позиция репозитория в топе
	stars: int  # Количество звёзд позиция репозитория в топе
	watchers: int  # Количество просмотров
	forks: int  # Количество форков
	open_issues: int  # Количество открытых issues
	language: Optional[str]  # Язык


class RepoDTO(RepoParsing):
	"""ДТО-класс для репозиториев GH"""
	id: Optional[str]						# Уникальное id репозитория (UUID в строке)
	position_prev: Optional[int]			# Предыдущая позиция репозитория в топе


class RepoUpload(RepoBase):
	"""Класс для передачи данных репозиториев GH по API (без лишних полей)"""
	repo: str  								# full_name репозитория
	owner: str 								# Владелец репозитория
	position_cur: int  						# Текущая позиция репозитория в топе
	position_prev: Optional[int] 			# Предыдущая позиция репозитория в топе
	stars: int  							# Количество звёзд позиция репозитория в топе
	watchers: int							# Количество просмотров
	forks: int  							# Количество форков
	open_issues: int  						# Количество открытых issues
	language: str  							# Язык
	