"""
    Настройки для прогона тестов - общие
"""
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.core.dependencies import get_actual_session_factory
from src.project import settings
from src.core.models import Base
from src.main import app

NUM_TESTS = 5

fake_engine = create_async_engine(url=settings.TEST_DATABASE_URL_async_sqlite,
                                  poolclass=NullPool,
                                  echo=settings.TEST_ECHO)
fake_session_factory = async_sessionmaker(bind=fake_engine,
                                          autoflush=False,
                                          autocommit=False,
                                          expire_on_commit=False)
metadata = Base.metadata
metadata.bind = fake_engine


def get_fake_session_factory():
    return fake_session_factory


app.dependency_overrides[get_actual_session_factory] = get_fake_session_factory


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with fake_engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with fake_engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope='session')
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope='session')
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        yield async_client


@pytest.fixture
async def session_factory() -> async_sessionmaker:
    session_factory = get_fake_session_factory()
    return session_factory


@pytest.fixture
async def clear_database() -> None:
    async with fake_engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
    async with fake_engine.begin() as conn:
        await conn.run_sync(metadata.create_all)