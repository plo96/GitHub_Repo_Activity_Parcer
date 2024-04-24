"""
	Создание и инициализация класса, ответственного за подключение к базе данных.
"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.project import settings


class DatabaseHelper:
	"""Класс, обеспечивающий подключение к базе данных с определёнными настройками."""
	
	def __init__(self, url: str, echo: bool):
		"""
		Инициализация DatabaseHelper(на основе SQLAlchemy).
		Создание движка подключения и фабрики сессий на основе этого движка.
		:param url: Адресс для подключения к базе данных.
		:param echo: Вывод отладочных сообщений в консоль (True/False)
		"""
		self._engine = create_async_engine(
			url=url,
			echo=echo,
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


db_helper = DatabaseHelper(url=settings.DATABASE_URL_async_sqlite, echo=settings.ECHO)
