from datetime import datetime

import pytest
from sqlalchemy import insert, select
from faker import Faker

from src.core.models import Repo, RepoActivity
from src.core.models.repos import LIMIT_TOP_REPOS_LIST

from tests.conftest import get_fake_session_factory

fake = Faker()


def get_new_repo() -> dict:
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


def get_new_repo_activity(list_of_repos_id: list) -> dict:
    return dict(
        repo_id=fake.random.choice(list_of_repos_id),
        # date=datetime(int(fake.year()), int(fake.month()), int(fake.day_of_month())),
        date=fake.date_time(),
        commits=fake.random.randint(1, 50),
        authors=', '.join([fake.user_name() for _ in range(fake.random.randint(1, 5))]),
    )


@pytest.fixture(scope='session')
def repos_url() -> str:
    return '/api/repos/'


@pytest.fixture
async def some_repos_added(clear_database: None) -> None:
    new_repos = [get_new_repo() for _ in range(LIMIT_TOP_REPOS_LIST)]
    session_factory = get_fake_session_factory()
    async with session_factory() as session:
        for new_repo in new_repos:
            stmt = insert(Repo).values(**new_repo)
            await session.execute(stmt)
        await session.flush()
        await session.commit()
        
        
@pytest.fixture
async def a_few_repos_added(clear_database: None) -> None:
    new_repos = [get_new_repo() for _ in range(LIMIT_TOP_REPOS_LIST - 1)]
    session_factory = get_fake_session_factory()
    async with session_factory() as session:
        for new_repo in new_repos:
            stmt = insert(Repo).values(**new_repo)
            await session.execute(stmt)
        await session.flush()
        await session.commit()


@pytest.fixture
async def some_repo_activities_added(some_repos_added: None) -> None:
    session_factory = get_fake_session_factory()
    async with session_factory() as session:
        stmt = select(Repo.id)
        res = await session.execute(stmt)
        list_of_repos_id = res.scalars().all()
        new_repo_activities = [get_new_repo_activity(list_of_repos_id) for _ in range(LIMIT_TOP_REPOS_LIST * 10)]
        for new_repo_activity in new_repo_activities:
            stmt = insert(RepoActivity).values(**new_repo_activity)
            await session.execute(stmt)
        await session.flush()
        await session.commit()
        stmt = select(Repo.owner, Repo.repo)
        res = await session.execute(stmt)
        list_of_repos_key = res.all()
    return list_of_repos_key
      
        