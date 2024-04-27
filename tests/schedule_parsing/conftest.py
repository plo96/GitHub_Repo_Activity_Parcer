from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker
from faker import Faker

from src.core.schemas import RepoParsing, RepoActivityParsing
from src.schedule.schedule_parser import ScheduleParser
from src.parsing.github import GithubParserRest
from src.core.models.repos import LIMIT_TOP_REPOS_LIST

fake = Faker()


def get_new_repo_parsing() -> dict:
    """Фейковый репозиторий для заполнения базы данных."""
    return dict(
        repo=fake.text(30),
        owner=fake.user_name(),
        position_cur=fake.random.randint(1, 100),
        stars=fake.random.randint(1, 5000),
        watchers=fake.random.randint(1, 5000),
        forks=fake.random.randint(1, 50),
        open_issues=fake.random.randint(0, 50),
        language=fake.language_name(),
    )


def get_new_repo_activity_parsing(
        used_dates: list,
) -> dict:
    """Фейковая история активности репозитория для случайного репозитория из набора."""
    new_date = fake.date_time().date()
    while new_date in used_dates:
        new_date = fake.date_time().date()
    used_dates.append(new_date)
    return dict(
        date=new_date,
        commits=fake.random.randint(1, 50),
        authors=[fake.user_name() for _ in range(fake.random.randint(1, 5))],
    )


@pytest.fixture(scope="session")
def fake_new_top_repos_parsing() -> list[RepoParsing]:
    fake_new_top_repos_parsing: list[RepoParsing] = []
    for _ in range(LIMIT_TOP_REPOS_LIST):
        fake_new_top_repos_parsing.append(RepoParsing.model_validate(get_new_repo_parsing()))
    return fake_new_top_repos_parsing


@pytest.fixture(scope="session")
def fake_new_repo_activities_parsing() -> list[RepoActivityParsing]:
    fake_new_repo_activities_parsing: list[RepoActivityParsing] = []
    for _ in range(fake.random.randint(1, 10)):
        used_dates: list = []
        fake_new_repo_activities_parsing.append(
            RepoActivityParsing.model_validate(
                get_new_repo_activity_parsing(
                    used_dates=used_dates,
                )
            )
        )
    return fake_new_repo_activities_parsing


@pytest.fixture(scope="session")
def fake_gh_parser(
        fake_new_top_repos_parsing: list[RepoParsing],
        fake_new_repo_activities_parsing: list[RepoActivityParsing],
) -> GithubParserRest:
    fake_gh_parser = GithubParserRest()
    fake_gh_parser.parsing_top = AsyncMock(return_value=fake_new_top_repos_parsing)
    fake_gh_parser.parsing_activities = AsyncMock(return_value=fake_new_repo_activities_parsing)
    return fake_gh_parser


@pytest.fixture(scope="session")
def fake_schedule_parser(
        session_factory: async_sessionmaker,
        fake_gh_parser: GithubParserRest,
) -> ScheduleParser:
    return ScheduleParser(
        parser=fake_gh_parser,
        session_factory=session_factory,
        pause_value=0,
    )
