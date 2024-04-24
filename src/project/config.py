"""
    Настройки для приложения.
    Корневая директория (HOME_DIR) - определяется исходя из положения данного файла.
    Создание и инициализация класса для импорта и валидации данных из .env файла.
    Дополнительные общие параметры для приложения задаются через свойства (@property).
"""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

HOME_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    """Класс, содержащий основные настройки для приложения."""
    model_config = SettingsConfigDict(env_file=f"{HOME_DIR}/.env")

    SQLITE_NAME: str
    TEST_SQLITE_NAME: str

    ECHO: bool
    TEST_ECHO: bool

    API_KEY: str

    @property
    def DATABASE_URL_async_sqlite(self) -> str:
        """URL для подключения к БД (aiosqlite)."""
        return f"sqlite+aiosqlite:///{HOME_DIR}/src/database/sqlite_db/{self.SQLITE_NAME}"

    @property
    def DATABASE_URL_sqlite(self) -> str:
        """URL для подключения к БД (sqlite3) - синхронный вариант для реализации миграций."""
        return f"sqlite:///{HOME_DIR}/src/database/sqlite_db/{self.SQLITE_NAME}"

    @property
    def TEST_DATABASE_URL_async_sqlite(self) -> str:
        """URL для подключения к тестовой БД (aiosqlite)."""
        return f"sqlite+aiosqlite:///{HOME_DIR}/src/database/sqlite_db/{self.TEST_SQLITE_NAME}"

    @property
    def HOME_DIR(self) -> str:
        """Корневая директория проекта."""
        return str(HOME_DIR.absolute())
    
    @property
    def MAX_PARSING_TRYING(self) -> int:
        """Максимальное число попыток в случае неудачи при парсинге."""
        return 5


settings = Settings()               # type: ignore
