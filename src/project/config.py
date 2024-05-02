"""
    Настройки для приложения.
    Корневая директория (HOME_DIR) - определяется исходя из положения данного файла.
    Создание и инициализация класса для импорта и валидации данных из .env файла.
    Дополнительные общие параметры для приложения задаются через свойства (@property).
"""
from pathlib import Path
from pydantic_settings import BaseSettings

HOME_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    """Класс, содержащий основные настройки для приложения."""
    APP_HOST_PORT: int = 8000

    DB_PORT: int
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    SQLITE_NAME: str

    ECHO: bool
    TEST_ECHO: bool

    API_KEY: str = ""

    FORCED_PREVENTIVES_PARSING: bool

    @property
    def DATABASE_URL_ASYNCPG(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_PSYCOPG_SYNC(self) -> str:
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_PSYCOPG_ASYNC(self) -> str:
        return f"postgresql+psycopg_async://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_async_sqlite(self) -> str:
        """URL для подключения к БД (aiosqlite)."""
        return f"sqlite+aiosqlite:///{HOME_DIR}/src/database/sqlite_db/{self.SQLITE_NAME}"

    @property
    def DATABASE_URL_sqlite(self) -> str:
        """URL для подключения к БД (sqlite3) - синхронный вариант для реализации миграций."""
        return f"sqlite:///{HOME_DIR}/src/database/sqlite_db/{self.SQLITE_NAME}"

    @property
    def HOME_DIR(self) -> str:
        """Корневая директория проекта."""
        return str(HOME_DIR.absolute())


settings = Settings()               # type: ignore
