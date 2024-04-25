from datetime import datetime, timedelta
from random import choice

import pytest
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.layers.repositories import RepoActivitiesRepository
from src.core.models import RepoActivity, Repo
from tests.conftest import NUM_TESTS


@pytest.mark.parametrize("_", range(NUM_TESTS))
async def test_get_repo_activities(
		_,
		some_repo_activities_added: None,
		session_factory: async_sessionmaker,
		owners_repos_with_activities: list[tuple],
		since_until: tuple,

):
	owner, repo = choice(owners_repos_with_activities)
	since, until = since_until
	until = until + timedelta(1)
	async with session_factory() as session:
		activities_list = await RepoActivitiesRepository.get_repo_activities(
			session=session,
			owner=owner,
			repo=repo,
			since=since,
			until=until,
		)
		for index, activity in enumerate(activities_list):
			activity = activity._asdict()
			activity["date"] = datetime.fromisoformat(activity["date"])
			activities_list[index] = activity
		
		stmt = select(
			RepoActivity
		).join(
			Repo,
			RepoActivity.repo_id == Repo.id,
		).filter_by(
			owner=owner,
			repo=repo,
		)
		res = await session.execute(stmt)
		res = res.scalars().all()
		for index, entity in enumerate(res):
			entity_dict = entity.__dict__
			entity_dict.pop('_sa_instance_state')
			res[index] = entity_dict
		assert all([activity in activities_list for activity in res])


async def test_delete_all_activities(
		session_factory: async_sessionmaker,
		some_repo_activities_added: None,
):
	async with session_factory() as session:
		stmt = select(RepoActivity)
		res = await session.execute(stmt)
		assert res.scalars().all()
		
		await RepoActivitiesRepository.delete_all_activities(
			session=session,
		)
		
		stmt = select(RepoActivity)
		res = await session.execute(stmt)
		assert not res.scalars().all()


@pytest.mark.parametrize("_", range(NUM_TESTS))
async def test_add_activity(
		_,
		session_factory: async_sessionmaker,
		new_repo_activity: dict,
):
	async with session_factory() as session:
		stmt = select(RepoActivity).filter_by(**new_repo_activity)
		res = await session.execute(stmt)
		assert not res.scalars().one_or_none()
		
		await RepoActivitiesRepository.add_activity(
			session=session,
			repo_activity_dict=new_repo_activity,
		)
		
		stmt = select(RepoActivity).filter_by(**new_repo_activity)
		res = await session.execute(stmt)
		assert res.scalars().one_or_none()


async def test_get_min_activity_date(
		some_repo_activities_added,
		session_factory: async_sessionmaker,
		since_until: tuple,
):
	since, _ = since_until
	async with session_factory() as session:
		res = await RepoActivitiesRepository.get_min_activity_date(
			session=session,
		)
		
		assert datetime.fromisoformat(res._tuple()[0]).date() == since
		
		stmt = text("DELETE FROM repo_activities")
		await session.execute(stmt)
		
		res = await RepoActivitiesRepository.get_min_activity_date(
			session=session,
		)
		
		assert not res


async def test_get_max_activity_date(
		some_repo_activities_added,
		session_factory: async_sessionmaker,
		since_until: tuple,
):
	_, until = since_until
	async with session_factory() as session:
		res = await RepoActivitiesRepository.get_max_activity_date(
			session=session,
		)
		
		assert datetime.fromisoformat(res._tuple()[0]).date() == until
		
		stmt = text("DELETE FROM repo_activities")
		await session.execute(stmt)
		
		res = await RepoActivitiesRepository.get_min_activity_date(
			session=session,
		)
		
		assert not res
