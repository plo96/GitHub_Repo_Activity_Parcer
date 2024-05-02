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
    APP_HOST_PORT: int

    DB_PORT: int
    DB_HOST: str
    DB_USER: str
    DB_NAME: str
    TEST_DB_NAME: str
    DB_PASSWORD: str

    ECHO: bool
    TEST_ECHO: bool

    API_KEY: str

    @property
    def DATABASE_URL_PSYCOPG_SYNC(self) -> str:
        """URL для подключения к БД через psycopg3 (синхронный вариант для миграций)"""
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_PSYCOPG_ASYNC(self) -> str:
        """URL для подключения к БД через psycopg3 (асинхронный вариант для API)"""
        return f"postgresql+psycopg_async://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_PSYCOPG_ASYNC_TEST(self) -> str:
        """URL для подключения к БД через psycopg3 (асинхронный вариант для тестов)"""
        return f"postgresql+psycopg_async://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.TEST_DB_NAME}"

    @property
    def HOME_DIR(self) -> str:
        """Корневая директория проекта."""
        return str(HOME_DIR.absolute())


settings = Settings()               # type: ignore
