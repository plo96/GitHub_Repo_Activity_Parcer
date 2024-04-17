"""
	Сервисы для осуществления бизнес-логики работ с репозиториями GitHub
"""
from datetime import date
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
import requests as req

from src.core.schemas import RepoDTO, RepoActivityDTO
from src.layers.repositories import ReposRepository


class RepoService:
	
	@staticmethod
	async def get_top_100_repos(
			session: AsyncSession,
			param: Optional[str],
	) -> list[RepoDTO]:
		result = await ReposRepository.get_repos_sorted_by_param(session=session, param=param)
		
		# keys = RepoDTO.model_fields.keys()
		# dict(entity.tuple)
		dict
		# print(result[0].tuple)
		# print(RepoDTO.model_fields.keys())
		return list([RepoDTO.model_validate(entity.tuple) for entity in result])
	
	@staticmethod
	async def get_activity(
			session: AsyncSession,
			owner: str,
			repo: str,
			since: date,
			until: date,
	) -> list[RepoActivityDTO]:
		...
