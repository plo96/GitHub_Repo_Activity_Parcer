from datetime import date
from uuid import UUID

from pydantic import BaseModel


class RepoActivityBase(BaseModel):
	"""Базовый класс для активности репозиториев GH"""
	pass


class RepoActivityDTO(RepoActivityBase):
	"""DTO-класс для активности репозиториев GH"""
	date: date				# Конкретная дата
	commits: int			# Количество коммитов за конкретный день
	authors: list[str]		# Список авторов, которые выполняли коммиты