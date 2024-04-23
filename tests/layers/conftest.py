from datetime import date

import pytest
from sqlalchemy import insert, select, join
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.exc import IntegrityError
from faker import Faker

from src.core.models import Repo, RepoActivity
from src.core.models.get_default import get_str_uuid
from src.core.models.repos import LIMIT_TOP_REPOS_LIST

fake = Faker()


def get_new_repo() -> dict:
    """Фейковый репозиторий для заполнения базы данных"""
    return dict(
        repo=fake.text(30),
        owner=fake.user_name(),
        position_cur=fake.random.randint(1, 100),
        position_prev=fake.random.randint(1, 100),
        stars=fake.random.randint(1, 5000),
        watches=fake.random.randint(1, 5000),
        forks=fake.random.randint(1, 50),
        open_issues=fake.random.randint(0, 50),
        language=fake.language_name(),
    )


def get_new_repo_activity(
        list_of_repos_id: list,
) -> dict:
    """Фейковая история активности репозитория для случайного репозитория из набора"""
    return dict(
        repo_id=fake.random.choice(list_of_repos_id),
        date=fake.date_time().date(),
        commits=fake.random.randint(1, 50),
        authors=', '.join([fake.user_name() for _ in range(fake.random.randint(1, 5))]),
    )


@pytest.fixture
async def new_repo() -> dict:
    """Фикстура для возвращения ПОЛНОГО словаря для фейкового репозитория"""
    new_repo = get_new_repo()
    new_repo["id"] = get_str_uuid()
    return new_repo


@pytest.fixture(scope='session')
def repos_url() -> str:
    """URL для запросов по репозиториям"""
    return '/api/repos/'


@pytest.fixture
async def owners_repos(
        session_factory: async_sessionmaker,
) -> list[tuple]:
    """Список кортежей с парами владелец/репозиторий для репозиториев с изменениями"""
    async with (session_factory() as session):
        stmt = (
            select(
                Repo.owner,
                Repo.repo,
            )
            .select_from(
                join(
                    Repo,
                    RepoActivity,
                    Repo.id == RepoActivity.repo_id,
                )
            )
        )
        res = await session.execute(stmt)
        owners_repos = [entity._tuple() for entity in res.all()]        # noqa
        return owners_repos


@pytest.fixture
async def since_until(
        session_factory: async_sessionmaker,
) -> tuple[date, date]:
    """Кортеж с минимальной и максимальной датами для репозиториев с изменениями"""
    async with session_factory() as session:
        stmt = select(RepoActivity.date).order_by(RepoActivity.date)
        result = await session.execute(stmt)
        all_dates = list(result.scalars().all())
        since, until = (all_dates[0].date(), all_dates[-1].date())
        return since, until


@pytest.fixture
async def some_repos_added(
        clear_database: None,
        session_factory: async_sessionmaker,
) -> None:
    """Добавляет в базу данных необходимое число фейковых репозиториев"""
    new_repos = [get_new_repo() for _ in range(LIMIT_TOP_REPOS_LIST)]
    async with session_factory() as session:
        for new_repo in new_repos:
            stmt = insert(Repo).values(**new_repo)
            await session.execute(stmt)
        await session.flush()
        await session.commit()
        
        
@pytest.fixture
async def a_few_repos_added(
        clear_database: None,
        session_factory: async_sessionmaker,
) -> None:
    """Добавляет в базу данных меньшее, чем требуется, число фейковых репозиториев"""
    new_repos = [get_new_repo() for _ in range(LIMIT_TOP_REPOS_LIST - 1)]
    async with session_factory() as session:
        for new_repo in new_repos:
            stmt = insert(Repo).values(**new_repo)
            await session.execute(stmt)
        await session.flush()
        await session.commit()


@pytest.fixture
async def some_repo_activities_added(
        some_repos_added: None,
        session_factory: async_sessionmaker,
) -> None:
    """Добавляет в базу данных фейковую историю изменений для фейковых репозиториев"""
    
    async with session_factory() as session:
        stmt = select(Repo.id)
        res = await session.execute(stmt)
        list_of_repos_id = list(res.scalars().all())
        for _ in range(LIMIT_TOP_REPOS_LIST * 3):
            while True:
                try:
                    new_repo_activity = get_new_repo_activity(list_of_repos_id)
                    stmt = insert(RepoActivity).values(**new_repo_activity)
                    await session.execute(stmt)
                    break
                except IntegrityError:
                    print("Unique constraint failed, reload...")
                    
        await session.flush()
        await session.commit()
     