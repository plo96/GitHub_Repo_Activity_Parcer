from sqlalchemy import text, bindparam, Row
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import Repo


class ReposRepository:
	"""Репозиторий на осное SQLALchemy для репозиториев GH"""
	model = Repo
	
	@staticmethod
	async def get_repos_sorted_by_param(
			session: AsyncSession,
			param: str = None,
	) -> list[Row]:
		if not param or param not in Repo.__annotations__.keys():
			param = "stars"
		stmt = text(f"SELECT * FROM repos ORDER BY {param} DESC")
		res = await session.execute(stmt)
		return list(res.all())
