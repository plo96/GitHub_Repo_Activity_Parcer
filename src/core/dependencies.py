"""
	Основные зависимости, используемые в приложении.
"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.database import db_helper


def get_actual_session_factory() -> async_sessionmaker:
	"""Получение актуальной фабрики сессий к базе данных."""
	return db_helper.get_session_factory()


async def get_session(
		session_factory: async_sessionmaker = Depends(get_actual_session_factory),
) -> AsyncSession:
	"""
	Получение сессии к базе данных исходя из актуальной фабрики сессий.
	Передача сессии внутри контекстного менеджера для автоматического закрытия.
	"""
	async with session_factory() as session:
		yield session
