from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Uuid

from .base import Base


class RepoActivity(Base):
	"""ОРМ-модель для активности репозиториев GH"""
	__tablename__ = "repo_activities"
	repo_id: Mapped[UUID] = mapped_column(  	# уникальный id репозитория
		Uuid,
		ForeignKey("repos.id"),
		primary_key=True,
	)
	date: Mapped[datetime] = mapped_column(		# Конкретная дата
		primary_key=True,
	)
	commits: Mapped[int]						# Количество коммитов за конкретный день
	authors: Mapped[str]						# Список авторов, которые выполняли коммиты
	