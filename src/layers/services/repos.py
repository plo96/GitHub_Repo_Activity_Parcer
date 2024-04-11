"""
	Сервисы для осуществления бизнес-логики работ с репозиториями GitHub
"""
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
import requests as req

from src.core.schemas import RepoDTO, RepoActivityDTO


class RepoService:
	
	@staticmethod
	async def get_top_100_repos(
			session: AsyncSession,
	) -> list[RepoDTO]:
		...
	
	@staticmethod
	async def get_activity(
			session: AsyncSession,
			owner: str,
			repo: str,
			since: date,
			until: date,
	) -> list[RepoActivityDTO]:
		...
