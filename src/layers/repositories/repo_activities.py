from datetime import datetime

from sqlalchemy import text, Row
from sqlalchemy.ext.asyncio import AsyncSession


class RepoActivitiesRepository:
	"""Репозиторий на основе SQLAlchemy для активности репозиториев GH"""
	
	@staticmethod
	async def get_repo_activities(
			session: AsyncSession,
			owner: str,
			repo: str,
			since: datetime,
			until: datetime,
	) -> list[Row]:
		"""Метод для выгрузки активности конкретного репозитория по дням"""
		stmt = text(
			f"""SELECT date, commits, authors FROM repo_activities
			JOINED repos ON repo_activities.repo_id == repos.id
			WHERE repos.owner == {owner}, repos.repo == {repo}, {since} <= repo_activities.date <= {until}
			"""
		)
		res = await session.execute(stmt)
		return list(res.all())
	