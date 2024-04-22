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
	
	@staticmethod
	async def get_param(
			session: AsyncSession,
			owner: str,
			repo: str,
			param: str,
	) -> Row | None:
		"""Метод для возврата заданного параметра репозитория"""
		stmt = text(
			f"""SELECT {param}	FROM repos
				WHERE repo == "{repo}" AND owner == "{owner}" """
		)
		res = await session.execute(stmt)
		return res.scalars().one_or_none()
	
	@staticmethod
	async def delete_all(
			session: AsyncSession,
	) -> None:
		"""Метод для удаления текущего топа репозиториев"""
		stmt = text(
			"""DELETE FROM repos"""
		)
		await session.execute(stmt)
		await session.flush()
	
	@staticmethod
	async def add_one(
			session: AsyncSession,
			new_repo: dict,
	) -> None:
		"""Метод для добавления одного репозитория"""
		stmt = text(
			f"""INSERT INTO repos
				VALUES {", ".join(str(value) for value in new_repo.values())} """
		)
		await session.execute(stmt)
		await session.flush()
		