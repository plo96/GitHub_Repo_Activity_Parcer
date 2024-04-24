"""
	Класс для реализации способов взаимодействия с БД для сущности репозитория.
"""
from typing import Any

from sqlalchemy import text, Row
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import Repo
from src.core.models.repos import DEFAULT_SORT_PARAM, LIMIT_TOP_REPOS_LIST


class ReposRepository:
	"""Репозиторий на осное SQLAlchemy для репозиториев GH."""
	
	@staticmethod
	async def get_repos_sorted_by_param(
			session: AsyncSession,
			param: str = DEFAULT_SORT_PARAM,
	) -> list[Row]:
		"""
		Выгрузка топа репозиториев с сортировкой по заданному параметру.
		:param session: Сессия для доступа к БД.
		:param param: Параметр по которому осуществляется сортировка. По умолчанию - количество звёзд.
		:return: Список строк SQLAlchemy если что-то найдено в базе.
				 Пустой список если ничего не найдено.
		"""
		if param not in Repo.__annotations__.keys() or param == "id":
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
		"""
		Проверка наличия комбинации владелец+репозиторий в базе.
		:param session: Сессия для доступа к БД.
		:param owner: Имя владельца репозитория на GitHub.
		:param repo: full_name репозитория на GitHub.
		:return: True - если искомая комбинация присутствует в базе.
				 False - если искомая комбинация jncencndetn в базе.
		"""
		stmt = text(
			f"""SELECT * FROM repos
				WHERE repos.owner == "{owner}" AND repos.repo == "{repo}" """
		)
		res = await session.execute(stmt)
		return bool(res.all())
	
	@staticmethod
	async def get_param(
			session: AsyncSession,
			owner: str,
			repo: str,
			param: str,
	) -> Any | None:
		"""
		Возврат заданного параметра репозитория.
		:param session: Сессия для доступа к БД.
		:param owner: Имя владельца репозитория на GitHub.
		:param repo: full_name репозитория на GitHub.
		:param param: Запрашиваемый параметр.
		:return: Значение запрашиваемого параметра если удалось его найти.
				 None если такого параметра нет в модели или не найден запрашиваемый репозиторий.
		"""
		if param not in Repo.__annotations__.keys():
			return None
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
		"""
		Удаление текущего топа репозиториев.
		:param session: Сессия для доступа к БД.
		:return: None.
		"""
		stmt = text(
			"""DELETE FROM repos"""
		)
		await session.execute(stmt)
		await session.flush()
	
	@staticmethod
	async def add_one(
			session: AsyncSession,
			repo_dict: dict,
	) -> None:
		"""
		Добавление одного репозитория.
		:param session: Сессия для доступа к БД.
		:param repo_dict: Словарь с значениями полей для модели репозитория.
		:return: None.
		"""
		stmt = text(
			f"""INSERT INTO repos ({", ".join(str(value) for value in repo_dict.keys())})
				VALUES ({", ".join(f'"{value}"' for value in repo_dict.values())}) """
		)
		await session.execute(stmt)
		await session.flush()
		