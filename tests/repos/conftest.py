import pytest
from sqlalchemy import insert, text
from faker import Faker

from src.core.models import Repo
from tests.conftest import get_fake_session_factory, NUM_REPOS

fake = Faker()


def get_new_repo() -> dict:
	return dict(
		repo=fake.text(20),
		owner=fake.user_name(),
		position_cur=fake.random.randint(1, 100),
		position_prev=fake.random.randint(1, 100),
		stars=fake.random.randint(1, 5000),
		watches=fake.random.randint(1, 5000),
		forks=fake.random.randint(1, 50),
		open_issues=fake.random.randint(0, 50),
		language=fake.language_name(),
	)


@pytest.fixture(scope='session')
def repos_url() -> str:
    return '/api/repos/'


@pytest.fixture
async def some_repo_added(clear_database: None) -> None:
	new_repos = [get_new_repo() for _ in range(NUM_REPOS)]
	session_factory = get_fake_session_factory()
	async with session_factory() as session:
		for new_repo in new_repos:
			stmt = insert(Repo).values(**new_repo)
			await session.execute(stmt)
		await session.commit()
		