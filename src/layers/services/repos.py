"""
	Сервисы для осуществления бизнес-логики работ с репозиториями GitHub
"""
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schemas import RepoDTO
from src.core.models.repos import LIMIT_TOP_REPOS_LIST
from src.project.exceptions import TooFewRepos
from src.layers.repositories import ReposRepository


class RepoService:
	
	@staticmethod
	async def get_top_repos(
			session: AsyncSession,
			param: Optional[str],
	) -> list[RepoDTO]:
		result = await ReposRepository.get_repos_sorted_by_param(session=session, param=param)
		if len(result) < LIMIT_TOP_REPOS_LIST:
			raise TooFewRepos(limit=LIMIT_TOP_REPOS_LIST, current_len=len(result))
		result = [entity._asdict() for entity in result]										# noqa
		[entity.__delitem__('id') for entity in result]
		return [RepoDTO.model_validate(entity) for entity in result]
