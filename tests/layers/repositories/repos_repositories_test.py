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
		res = list(res.scalars().all())
		res.reverse()
		for index, entity in enumerate(res):
			entity_dict = entity.__dict__
			entity_dict.pop('_sa_instance_state')
			print(top_list)
			print()
			print(tuple(entity_dict.values()))
			assert all([value in top_list[index] for value in tuple(entity_dict.values())])
		# assert all([entity in top_list for entity in res])



[
	('2c50c0e8-02ed-4e56-9319-2c42f5bbc1fe', 'Like property see.', 'danielmathews', 90, 90, 3460, 1499, 29, 44, 'Afar'),
	('51afbfcb-e9a3-4658-833e-c16254d82536', 'Bag professional energy.', 'robert89', 49, 74, 25, 4178, 18, 33, 'Sanskrit'),
	('0be30a5b-9f8c-49a2-abc9-2b54d8f82929', 'Baby image tend range reason.', 'david60', 14, 38, 194, 3226, 18, 32, 'Breton'),
	('b605e9aa-1fe0-45f1-9095-10b182e64baf', 'White evening study.', 'stevensonryan', 19, 45, 46, 3840, 13, 18, 'Ukrainian'), (
	'c063f6d6-406c-4abd-918a-40430d126449', 'Build strategy address south.', 'hawkinsbrenda', 44, 10, 296, 1442, 12, 38, 'Limburgan')
]

(90, '2c50c0e8-02ed-4e56-9319-2c42f5bbc1fe', 'Like property see.', 3460, 29, 'Afar', 'danielmathews', 90, 1499, 44)
[
	('2c50c0e8-02ed-4e56-9319-2c42f5bbc1fe', 'Like property see.', 'danielmathews', 90, 90, 3460, 1499, 29, 44, 'Afar'),
	('51afbfcb-e9a3-4658-833e-c16254d82536', 'Bag professional energy.', 'robert89', 49, 74, 25, 4178, 18, 33, 'Sanskrit'),
	('0be30a5b-9f8c-49a2-abc9-2b54d8f82929', 'Baby image tend range reason.', 'david60', 14, 38, 194, 3226, 18, 32, 'Breton'),
	('b605e9aa-1fe0-45f1-9095-10b182e64baf', 'White evening study.', 'stevensonryan', 19, 45, 46, 3840, 13, 18, 'Ukrainian'),
	('c063f6d6-406c-4abd-918a-40430d126449', 'Build strategy address south.', 'hawkinsbrenda', 44, 10, 296, 1442, 12, 38, 'Limburgan')
 ]

(14, '0be30a5b-9f8c-49a2-abc9-2b54d8f82929', 'Baby image tend range reason.', 194, 18, 'Breton', 'david60', 38, 3226, 32)








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
		
		assert res.__getattribute__(param) == param_value


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
