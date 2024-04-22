from random import choice

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.layers.repositories import ReposRepository
from src.core.models import Repo
from tests.conftest import NUM_TESTS


@pytest.mark.parametrize("_", range(NUM_TESTS))
async def test_add_one(
		_,
		session_factory: async_sessionmaker,
		new_repo: dict,
):
	async with session_factory() as session:
		
		await ReposRepository.add_one(
			session=session,
			new_repo=new_repo,
		)
		
		stmt = select(Repo).filter_by(**new_repo)
		res = await session.execute(stmt)
		
		print(res)
		res = res.scalars().one_or_none()
		print(res)
		assert res == tuple(new_repo.values())


async def test_delete_all(
		session_factory: async_sessionmaker,
		some_repos_added: None,
):
	async with session_factory() as session:
		stmt = select(Repo)
		res = await session.execute(stmt)
		assert res.scalars().all()
		
		await ReposRepository.delete_all(
			session=session,
		)
		
		stmt = select(Repo)
		res = await session.execute(stmt)
		assert not res.scalars().all()


@pytest.mark.parametrize("_", range(NUM_TESTS))
async def test_get_param(
		_,
		session_factory: async_sessionmaker,
		new_repo: dict,
):
	async with session_factory() as session:
		
		await ReposRepository.add_one(
			session=session,
			new_repo=new_repo,
		)
		
		await ReposRepository.get_param(
			session=session,
			owner=new_repo["owner"],
			repo=new_repo["repo"],
			param=choice(list(new_repo.keys())),
		)
		
		stmt = select(Repo).filter_by(**new_repo)
		res = await session.execute(stmt)
		assert not res.scalars().all()

