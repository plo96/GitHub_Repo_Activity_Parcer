from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.database import db_helper


def get_actual_session_factory() -> async_sessionmaker:
	return db_helper.get_session_factory()


async def get_session(session_factory: async_sessionmaker = Depends(get_actual_session_factory)) -> AsyncSession:
	async with session_factory() as session:
		yield session
