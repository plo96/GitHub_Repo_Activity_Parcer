from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Repo(Base):
	"""ОРМ-модель для репозиториев GH"""
	__tablename__ = "repos"
	repo: Mapped[str] = mapped_column(		# full_name репозитория
		primary_key=True,
	)
	owner: Mapped[str]  					# владелец репозитория
	position_cur: Mapped[int]  				# Текущая позиция репозитория в топе
	position_prev: Mapped[int]  			# Предыдущая позиция репозитория в топе
	stars: Mapped[int]  					# Количество звёзд позиция репозитория в топе
	watches: Mapped[int] 					# Количество просмотров
	forks: Mapped[int]  					# Количество форков
	open_issues: Mapped[int]  				# Количество открытых issues
	language: Mapped[str]  					# Язык
	