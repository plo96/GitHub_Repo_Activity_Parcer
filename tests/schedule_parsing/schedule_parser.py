from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select

from src.core.schemas import RepoParsing, RepoActivityParsing
from src.core.models import Repo, RepoActivity
from src.schedule.schedule_parser import ScheduleParser


async def test_schedule_parser_parsing(
		fake_schedule_parser: ScheduleParser,
):
	"""
	Тест метода parsing класса SchedulerParser.
	:param fake_schedule_parser: Тестовый объект класса SchedulerParser.
	"""
	new_top_repos, new_repos_activities = await fake_schedule_parser.parsing()
	
	assert isinstance(new_top_repos, list)
	assert all(
		[
			isinstance(new_repo, RepoParsing)
			for new_repo in new_top_repos
		]
	)
	assert isinstance(new_repos_activities, list)
	assert all(
		[
			isinstance(activity, RepoActivityParsing)
			for repo_activities in new_repos_activities
			for activity in repo_activities
		]
	)


async def test_schedule_parser_update_db(
		clear_database: None,
		session_factory: async_sessionmaker,
		fake_schedule_parser: ScheduleParser,
):
	"""
	Тест метода update_db класса SchedulerParser.
	:param clear_database: Очиситка БД перед тестом.
	:param session_factory: Сессия для доступа к БД.
	:param fake_schedule_parser: Тестовый объект класса SchedulerParser.
	"""
	new_top_repos, new_repos_activities = await fake_schedule_parser.parsing()

	await fake_schedule_parser.update_db(new_top_repos, new_repos_activities)
	
	async with session_factory() as session:
		stmt = select(Repo)
		res = await session.execute(stmt)
		res = res.scalars().all()
	repos_in_base: list = []
	for entity in res:
		repo = entity.__dict__
		repo.__delitem__('id'),
		repo.__delitem__('position_prev')
		repo.__delitem__('_sa_instance_state')
		repos_in_base.append(repo)
	
	assert all(new_repo.model_dump() in repos_in_base for new_repo in new_top_repos)
	
	async with session_factory() as session:
		stmt = select(RepoActivity)
		res = await session.execute(stmt)
		res = res.scalars().all()
		
		all_activities: list = []
		
		for entity in res:
			activity = entity.__dict__
			activity.__delitem__('_sa_instance_state')
			activity.__delitem__('repo_id')
			activity.__setitem__("date", (activity["date"].date()))
			activity.__setitem__("authors", list(activity['authors'].split(", ")))
			all_activities.append(activity)
		
		for repo_activities in new_repos_activities:
			for activity in repo_activities:
				assert activity.model_dump() in all_activities
				