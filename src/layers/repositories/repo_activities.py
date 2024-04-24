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
			f"""SELECT date, commits, authors FROM repo_activities
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
			f"""INSERT INTO repo_activities
				VALUES {", ".join(f'"{value}"' for value in repo_activity_dict.values())} """
		)
		await session.execute(stmt)
		await session.flush()
	