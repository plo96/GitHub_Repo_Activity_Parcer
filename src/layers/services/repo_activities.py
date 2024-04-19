from datetime import date, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schemas import RepoActivityDTO
from src.layers.repositories import RepoActivitiesRepository


class RepoActivitiesService:
	@staticmethod
	async def get_activity(
			session: AsyncSession,
			owner: str,
			repo: str,
			since: date,
			until: date,
	) -> list[RepoActivityDTO]:
		since = datetime(since.year, since.month, since.day)
		until = datetime(until.year, until.month, until.day)
		result = await RepoActivitiesRepository.get_repo_activities(
			session=session,
			owner=owner,
			repo=repo,
			since=since,
			until=until,
		)
		
		print(result)
		
		return None
