"""
	Класс для реализации способов взаимодействия с БД для сущности активности репозитория.
"""
from datetime import date

from sqlalchemy import text, Row
from sqlalchemy.ext.asyncio import AsyncSession


class RepoActivitiesRepository:
	"""Репозиторий на основе SQLAlchemy для активности репозиториев GH."""
	
	@staticmethod
	async def get_repo_activities(
			session: AsyncSession,
			owner: str,
			repo: str,
			since: date,
			until: date,
	) -> list[Row]:
		"""
		Выгрузка списка активностей конкретного репозитория по дням.
		:param session: Сессия для доступа к БД.
		:param owner: Имя владельца репозитория на GitHub.
		:param repo: full_name репозитория на GitHub.
		:param since: Начальная точка для выборки.
		:param until: Конечная точка для выборки.
		:return: Список строк SQLAlchemy если что-то найдено в базе.
				 Пустой список если ничего не найдено.
		"""
		stmt = text(
			f"""SELECT repo_id, date, commits, authors FROM repo_activities
			JOIN repos ON repo_activities.repo_id == repos.id
			WHERE repos.owner == "{owner}"
			AND repos.repo == "{repo}"
			AND repo_activities.date >= DATE("{since}")
			AND repo_activities.date <= DATE("{until}")
			"""
		)
		res = await session.execute(stmt)
		return list(res.all())
	
	@staticmethod
	async def delete_all_activities(
			session: AsyncSession,
	) -> None:
		"""
		Удаление всех активностей репозиториев.
		:param session: Сессия для доступа к БД.
		:return: None.
		"""
		stmt = text(
			"""DELETE FROM repo_activities"""
		)
		await session.execute(stmt)
		await session.flush()
	
	@staticmethod
	async def add_activity(
			session: AsyncSession,
			repo_activity_dict: dict,
	) -> None:
		"""
		Добавление одной активности одного репозитория.
		:param session: Сессия для доступа к БД.
		:param repo_activity_dict: Словарь с значениями полей для модели активности репозитория.
		:return: None.
		"""
		stmt = text(
			f"""INSERT INTO
			repo_activities ({", ".join(key for key in repo_activity_dict.keys())})
			VALUES
			({", ".join(f'"{value}"' for value in repo_activity_dict.values())}) """
		)
		await session.execute(stmt)
		await session.flush()
	
	@staticmethod
	async def get_max_activity_date(
			session: AsyncSession,
	) -> Row | None:
		"""
		Максимальная дата из всех записей по активностям репозиториев.
		:param session: Сессия для доступа к БД.
		:return: Row с одним значением времени в строке.
				 None если в базе вообще нет данных по активностям репозиториев.
		"""
		stmt = text(
			"""SELECT repo_activities.date
			   FROM repo_activities
			   ORDER BY repo_activities.date DESC
			   LIMIT 1"""
		)
		res = await session.execute(stmt)
		res = res.one_or_none()
		return res
	
	@staticmethod
	async def get_min_activity_date(
			session: AsyncSession,
	) -> Row | None:
		"""
		Минимальная дата из всех записей по активностям репозиториев.
		:param session: Сессия для доступа к БД.
		:return:Row с одним значением времени в строке.
				None если в базе вообще нет данных по активностям репозиториев.
		"""
		stmt = text(
			"""SELECT repo_activities.date
			   FROM repo_activities
			   ORDER BY repo_activities.date ASC
			   LIMIT 1"""
		)
		res = await session.execute(stmt)
		res = res.one_or_none()
		return res
