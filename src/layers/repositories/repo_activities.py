from datetime import date

from sqlalchemy import text, Row
from sqlalchemy.ext.asyncio import AsyncSession


class RepoActivitiesRepository:
	"""Репозиторий на основе SQLAlchemy для активности репозиториев GH"""
	
	@staticmethod
	async def get_repo_activities(
			session: AsyncSession,
			owner: str,
			repo: str,
			since: date,
			until: date,
	) -> list[Row] | None:
		"""Метод для выгрузки активности конкретного репозитория по дням"""
		stmt = text(
			f"""SELECT date, commits, authors FROM repo_activities
			JOIN repos ON repo_activities.repo_id == repos.id
			WHERE repos.owner == "{owner}"
			AND repos.repo == "{repo}"
			AND repo_activities.date >= DATE("{since}")
			AND repo_activities.date <= DATE("{until}")
			"""
		)
		res = await session.execute(stmt)
		if not res:
			return
		return list(res.all())
	