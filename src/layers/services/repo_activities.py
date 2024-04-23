"""
	Сервис для осуществления бизнес-логики при работе с активностями репозиториев.
"""
from datetime import datetime, date

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schemas import RepoActivityUpload, RepoActivityDTO
from src.layers.repositories import RepoActivitiesRepository, ReposRepository
from src.project.exceptions import NoRepoActivities, NoRepoOwnerCombination, AddNewDataError


class RepoActivitiesService:
	"""
		Класс сервиса для осуществления бизнес-логики при работе с активностями репозиториев.
		Используются статические методы. Экземпляр класса не создаётся.
	"""
	
	@staticmethod
	async def get_activity(
			session: AsyncSession,
			owner: str,
			repo: str,
			since: date,
			until: date,
	) -> list[RepoActivityUpload]:
		"""
		Получение информации об активности в конкретном репозитории по дням за определённый промежуток времени.
		:param session: Сессия для доступа к БД.
		:param owner: Имя владельца репозитория на GitHub.
		:param repo: full_name репозитория на GitHub.
		:param since: Начальная точка для выборки.
		:param until: Конечная точка для выборки.
		:return:   Список моделей с активностями данного репозитория по дням в пределах запрашиваемого периода.
		"""
		result = await RepoActivitiesRepository.get_repo_activities(
			session=session,
			owner=owner,
			repo=repo,
			since=since,
			until=until,
		)
		
		if not result:
			if await ReposRepository.check_owner_repo_combination(
				session=session,
				owner=owner,
				repo=repo,
			):
				raise NoRepoActivities
			else:
				raise NoRepoOwnerCombination
		
		result = [entity._asdict() for entity in result]			# noqa
		
		for entity in result:
			entity["date"] = datetime.fromisoformat(entity["date"])
			entity['authors'] = list(entity['authors'].split(", "))
		
		result = [RepoActivityUpload.model_validate(entity) for entity in result]
		return result
	
	@staticmethod
	async def set_new_repo_activities(
			session: AsyncSession,
			new_repos_activities: list[list[RepoActivityDTO]],
	) -> None:
		"""
		Добавление нового списка активностей репозиториев в БД.
		:param session: сессия для доступа к БД.
		:param new_repos_activities: список со списками активностей для каждого репозитория.
		:return: None.
		"""
		
		try:
			await RepoActivitiesRepository.delete_all_activities(
				session=session
			)
			
			for repo_activities in new_repos_activities:
				for repo_activity in repo_activities:
					repo_activity_dict = repo_activity.model_dump()
					repo_activity_dict["authors"] = ", ".join(author for author in repo_activity_dict["authors"])
					await RepoActivitiesRepository.add_activity(
						session=session,
						repo_activity_dict=repo_activity_dict,
					)
		except Exception as _ex:
			print(_ex)
			raise AddNewDataError
			