from sqlalchemy import text, Row
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import Repo
from src.core.models.repos import DEFAULT_SORT_PARAM, LIMIT_TOP_REPOS_LIST


class ReposRepository:
	"""Репозиторий на осное SQLAlchemy для репозиториев GH"""
	
	@staticmethod
	async def get_repos_sorted_by_param(
			session: AsyncSession,
			param: str = None,
	) -> list[Row]:
		"""Метод для выгрузки топа репозиториев с сортировкой по параметру"""
		if not param or param not in Repo.__annotations__.keys() or param == "id":
			param = DEFAULT_SORT_PARAM
		stmt = text(
			f"""SELECT * FROM repos
				ORDER BY {param} DESC
				LIMIT {LIMIT_TOP_REPOS_LIST}"""
		)
		res = await session.execute(stmt)
		return list(res.all())
	
	@staticmethod
	async def check_owner_repo_combination(
			session: AsyncSession,
			owner: str,
			repo: str,
	) -> bool:
		"""Метод для проверки наличия комбинации владелец+репозиторий"""
		stmt = text(
			f"""SELECT * FROM repos
				WHERE repos.owner == "{owner}" AND repos.repo == "{repo}" """
		)
		res = await session.execute(stmt)
		return bool(res)
