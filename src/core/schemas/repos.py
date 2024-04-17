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
