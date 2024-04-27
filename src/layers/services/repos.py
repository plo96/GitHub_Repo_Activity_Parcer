"""
	Сервис для осуществления бизнес-логики при работе с репозиториями GitHub.
"""

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.get_default import get_str_uuid
from src.core.schemas import RepoDTO, RepoUpload, RepoParsing
from src.core.models.repos import LIMIT_TOP_REPOS_LIST
from src.project.exceptions import TooFewRepos, AddNewDataError
from src.layers.repositories import ReposRepository


class RepoService:
	"""
		Класс сервиса для осуществления бизнес-логики при работе с репозиториями GitHub.
		Используются статические методы. Экземпляр класса не создаётся.
	"""
	
	@staticmethod
	async def get_top_repos(
			session: AsyncSession,
			param: Optional[str],
	) -> list[RepoUpload]:
		"""
		Получения топа репозиториев из БД.
		Метод для ответа по API.
		:param session: Сессия для доступа к БД.
		:param param: Параметр по которому осуществляется сортировка. По умолчанию - количество звёзд.
		:return: Список моделей с репозиториям GitHub в запрашиваемом порядке.
				 Вызов ошибки TooFewRepos в случае если получени из базы меньше репозиториев, чем запрошено.
		"""
		result = await ReposRepository.get_repos_sorted_by_param(session=session, param=param)
		
		if len(result) < LIMIT_TOP_REPOS_LIST:
			raise TooFewRepos(limit=LIMIT_TOP_REPOS_LIST, current_len=len(result))
		
		result = [entity._asdict() for entity in result]										# noqa
		return [RepoUpload.model_validate(entity) for entity in result]
	
	@staticmethod
	async def set_new_top_repos(
			session: AsyncSession,
			new_top_repos: list[RepoParsing],
	) -> list[RepoDTO]:
		"""
		Обновление данных по топу репозиториев в БД.
		Метод для вызова из периодической задачи.
		Обновляет данные в списке репозиториев - добавляет аттрибуты 'position_prev' и 'id'.
		:param session: Сессия для доступа к БД.
		:param new_top_repos: Список с новым топом репозиториев GitHub, которые перезапишут имеющийся топ.
		:return: Список ДТО-объектов для репозиториев GitHub.
				 Вызов ошибки AddNewDataError в случае возникновения ошибки.
		"""
		
		try:
			new_top_repos_dto: list[RepoDTO] = []
			for new_repo in new_top_repos:
				position_prev = await ReposRepository.get_param(
					session=session,
					owner=new_repo.owner,
					repo=new_repo.repo,
					param="position_cur",
				)
				new_repo_dto_dict: dict = new_repo.model_dump()
				new_repo_dto_dict.__setitem__("position_prev", position_prev)
				new_repo_dto_dict.__setitem__("id", get_str_uuid())
				new_top_repos_dto.append(RepoDTO.model_validate(new_repo_dto_dict))
				
			await ReposRepository.delete_all(session=session)
			
			for new_repo in new_top_repos_dto:
				
				await ReposRepository.add_one(
					session=session,
					repo_dict=new_repo.model_dump(),
				)
		
			return new_top_repos_dto
		except Exception as _ex:
			print(_ex)
			raise AddNewDataError
			