from random import choice

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.layers.repositories import ReposRepository
from src.core.models import Repo
from tests.conftest import NUM_TESTS


@pytest.mark.parametrize(
	"param",
	[
		None,
		*list(Repo.__annotations__.keys()),
		"_smth_",
	]
)
async def test_get_repos_sorted_by_param(
		param: str | None,
		some_repos_added: None,
		session_factory: async_sessionmaker,
		
):
	async with session_factory() as session:
		top_list = await ReposRepository.get_repos_sorted_by_param(
			session=session,
			param=param,
		)
		
		if param in (None, "id", "_smth_"):
			stmt = select(Repo).order_by("stars")
			res = await session.execute(stmt)
		else:
			stmt = select(Repo).order_by(param)
			res = await session.execute(stmt)
		res = res.scalars().all()
		# for index, entity in enumerate(res):
		# 	res[index] = entity
		#
		# assert res == top_list


@pytest.mark.parametrize("_", range(NUM_TESTS))
async def test_check_owner_repo_combination(
		_,
		session_factory: async_sessionmaker,
		some_repos_added: None,
		owners_repos: list[tuple],
):
	
	real_owner_repo_pair = choice(owners_repos)
	
	fake_owner_repo_pair: tuple = ()
	owner = choice(owners_repos)[0]
	for owner_repo in owners_repos:
		if owner_repo[0] != owner:
			fake_owner_repo_pair = (owner, owner_repo[1])
			break
		else:
			print("Can not choose fake pair owner-repo.")
			assert 1 == 0
	
	async with session_factory() as session:
		assert await ReposRepository.check_owner_repo_combination(
			session=session,
			owner=real_owner_repo_pair[0],
			repo=real_owner_repo_pair[1],
		)
		
		assert not await ReposRepository.check_owner_repo_combination(
			session=session,
			owner=fake_owner_repo_pair[0],
			repo=fake_owner_repo_pair[1],
		)


@pytest.mark.parametrize("_", range(NUM_TESTS))
async def test_get_param(
		_,
		session_factory: async_sessionmaker,
		new_repo: dict,
):
	async with session_factory() as session:
		await ReposRepository.add_one(
			session=session,
			repo_dict=new_repo,
		)
		
		param: str = choice(list(new_repo.keys()))
		
		param_value = await ReposRepository.get_param(
			session=session,
			owner=new_repo["owner"],
			repo=new_repo["repo"],
			param=param,
		)
		
		res = await session.get(Repo, new_repo.get("id"))
		
		assert res.__getattribute__(__name=param) == param_value


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
async def test_add_one(
		_,
		session_factory: async_sessionmaker,
		new_repo: dict,
):
	async with session_factory() as session:
		await ReposRepository.add_one(
			session=session,
			repo_dict=new_repo,
		)
		
		res = await session.get(Repo, new_repo.get("id"))
		res = res.__dict__
		assert all(new_repo[key] == res[key] for key in new_repo.keys())
