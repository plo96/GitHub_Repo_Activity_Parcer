from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schemas import RepoActivityDTO
from src.layers.repositories import RepoActivitiesRepository, ReposRepository
from src.project.exceptions import NoRepoActivities, NoRepoOwnerCombination


class RepoActivitiesService:
	@staticmethod
	async def get_activity(
			session: AsyncSession,
			owner: str,
			repo: str,
			since: date,
			until: date,
	) -> list[RepoActivityDTO]:

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
			year = int(entity["date"][:4])
			mounth = int(entity["date"][5:7])
			day = int(entity["date"][8:10])
			
			entity["date"] = date(year, mounth, day)
			entity['authors'] = list(entity['authors'].split(", "))
		
		result = [RepoActivityDTO.model_validate(entity) for entity in result]
		
		return result
