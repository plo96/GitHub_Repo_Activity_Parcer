"""
	Сервисы для осуществления бизнес-логики работ с репозиториями GitHub
"""
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schemas import RepoDTO
from src.core.models.repos import LIMIT_TOP_REPOS_LIST
from src.project.exceptions import TooFewRepos, AddNewDataError
from src.layers.repositories import ReposRepository


class RepoService:
	
	@staticmethod
	async def get_top_repos(
			session: AsyncSession,
			param: Optional[str],
	) -> list[RepoDTO]:
		"""Метод получения топа репозиториев из БД"""
		result = await ReposRepository.get_repos_sorted_by_param(session=session, param=param)
		
		if len(result) < LIMIT_TOP_REPOS_LIST:
			raise TooFewRepos(limit=LIMIT_TOP_REPOS_LIST, current_len=len(result))
		
		result = [entity._asdict() for entity in result]										# noqa
		[entity.__delitem__('id') for entity in result]
		
		return [RepoDTO.model_validate(entity) for entity in result]
	
	@staticmethod
	async def set_new_top_repos(
			session: AsyncSession,
			new_top_repos: list[dict],
	) -> None:
		"""Метод обновления данных по топу репозиториев в БД
		   добавляет в список репозиториев присвоенное id в формате UUID"""
		
		try:
			for position, new_repo in enumerate(new_top_repos):
				new_repo["position_cur"] = position
				new_repo["position_prev"] = ReposRepository.get_param(
					session=session,
					owner=new_repo["owner"],
					repo=new_repo["repo"],
					param="position_cur",
				)
			
			await ReposRepository.delete_all(session=session)
			
			for new_repo in new_top_repos:
				
				await ReposRepository.add_one(
					session=session,
					new_repo=new_repo,
				)
				
				res = await ReposRepository.get_param(
					session=session,
					owner=new_repo["owner"],
					repo=new_repo["repo"],
					param="id",
				)
				new_id = str(res)
				if not new_id:
					raise AddNewDataError
				new_repo["id"] = UUID(new_id)
		except Exception as _ex:
			print(_ex)
			raise AddNewDataError
			