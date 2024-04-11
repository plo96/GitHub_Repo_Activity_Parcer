from datetime import date

from pydantic import BaseModel


class RepoBase(BaseModel):
	"""Базовый класс для репозиториев GH"""
	pass


class RepoDTO(RepoBase):
	"""ДТО-класс для репозиториев GH"""
	repo: str				# full_name репозитория
	owner: str				# владелец репозитория
	position_cur: int		# Текущая позиция репозитория в топе
	position_prev: int		# Предыдущая позиция репозитория в топе
	stars: int				# Количество звёзд позиция репозитория в топе
	watches: int			# Количество просмотров
	forks: int				# Количество форков
	open_issues: int		# Количество открытых issues
	language: str			# Язык


class RepoActivityDTO(RepoBase):
	"""DTO-класс для активности репозиториев GH"""
	date: date				# Конкретная дата
	commits: int			# Количество коммитов за конкретный день
	authors: list[str]		# Список авторов, которые выполняли коммиты
