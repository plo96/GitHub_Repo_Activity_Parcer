from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .get_default import get_str_uuid

DEFAULT_SORT_PARAM = "stars"
LIMIT_TOP_REPOS_LIST = 100


class Repo(Base):
	"""ОРМ-модель для репозиториев GH"""
	__tablename__ = "repos"
	id: Mapped[str] = mapped_column(		# уникальный id репозитория
		String,
		primary_key=True,
		default=get_str_uuid,
	)
	repo: Mapped[str] 						# full_name репозитория
	owner: Mapped[str] 						# владелец репозитория
	position_cur: Mapped[int]  				# Текущая позиция репозитория в топе
	position_prev: Mapped[int | None]  		# Предыдущая позиция репозитория в топе
	stars: Mapped[int]  					# Количество звёзд позиция репозитория в топе
	watches: Mapped[int] 					# Количество просмотров
	forks: Mapped[int]  					# Количество форков
	open_issues: Mapped[int]  				# Количество открытых issues
	language: Mapped[str]  					# Язык
