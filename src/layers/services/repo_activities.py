import datetime
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schemas import RepoActivityDTO, RepoActivityUpload
from src.layers.repositories import RepoActivitiesRepository, ReposRepository
from src.project.exceptions import NoRepoActivities, NoRepoOwnerCombination, AddNewDataError


class RepoActivitiesService:
	@staticmethod
	async def get_activity(
			session: AsyncSession,
			owner: str,
			repo: str,
			since: date,
			until: date,
	) -> list[RepoActivityUpload]:
		"""Метод для получения информации об активности в репозитории по дням"""
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
			# print(datetime.datetime.fromtimestamp(entity["date"]))
			year = int(entity["date"][:4])
			mounth = int(entity["date"][5:7])
			day = int(entity["date"][8:10])
			
			entity["date"] = date(year, mounth, day)
			entity['authors'] = list(entity['authors'].split(", "))
		
		result = [RepoActivityUpload.model_validate(entity) for entity in result]
		# TODO repo_id
		return result
	
	@staticmethod
	async def set_new_repo_activities(
			session: AsyncSession,
			new_repo_activities: list[list[dict]],
	) -> None:
		"""Метод добавления нового списка активностей репозиториев в БД"""
		
		try:
			await RepoActivitiesRepository.delete_all_activities(
				session=session
			)
			
			for activities_list in new_repo_activities:
				for repo_activity in activities_list:
					await RepoActivitiesRepository.add_activity(
						session=session,
						repo_activity=repo_activity,
					)
		except Exception as _ex:
			print(_ex)
			raise AddNewDataError
			