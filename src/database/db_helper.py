from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.project import settings


class DatabaseHelper:
	"""Класс, обеспечивающий подключение к базе данных с определёнными настройками"""
	
	def __init__(self, url: str, echo: str):
		self._engine = create_async_engine(
			url=url,
			echo=echo
		)
		
		self._session_factory = async_sessionmaker(
			bind=self._engine,
			autoflush=False,
			autocommit=False,
			expire_on_commit=False,
		)
	
	def get_session_factory(self) -> async_sessionmaker:
		"""Возвращает фабрику сессий для подключения к БД"""
		return self._session_factory


db_helper = DatabaseHelper(url=settings.DATABASE_URL_async_sqlite, echo=settings.ECHO)  # type: ignore
