from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from .base import Base


class RepoActivity(Base):
	"""ОРМ-модель для активности репозиториев GH"""
	__tablename__ = "repo_activities"
	repo: Mapped[str] = mapped_column(			# full_name репозитория
		ForeignKey("repos.repo"),
		primary_key=True,
	)
	date: Mapped[datetime] = mapped_column(		# Конкретная дата
		primary_key=True,
	)
	commits: Mapped[int]						# Количество коммитов за конкретный день
	authors: Mapped[str]						# Список авторов, которые выполняли коммиты
	