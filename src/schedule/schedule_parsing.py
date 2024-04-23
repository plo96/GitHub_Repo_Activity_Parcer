from fastapi_utilities import repeat_at

from src.project import settings
from src.project.exceptions import CustomException
from src.parsing.github import GithubParserRest
from src.layers.services import RepoService, RepoActivitiesService
from src.core.dependencies import get_actual_session_factory


@repeat_at(cron="0 7 * * *")
async def schedule_parsing() -> None:
	try:
		gh_parser = GithubParserRest(settings.API_KEY)
		
		new_top_repos = await gh_parser.parsing_top()
		
		new_repo_activities: list = []
		for repo in new_top_repos:
			new_repo_activities.append(
				await gh_parser.parsing_activities(
					repo=repo,
				)
			)
			
		session_factory = get_actual_session_factory()
		async with session_factory() as session:
			
			try:
				await RepoService.set_new_top_repos(
					session=session,
					new_top_repos=new_top_repos,
				)
			
				for repo, activities_list in zip(new_top_repos, new_repo_activities):
					for activity in activities_list:
						activity.repo_id = repo.id
				
				await RepoActivitiesService.set_new_repo_activities(
					session=session,
					new_repo_activities=new_repo_activities,
				)
			
				await session.commit()
			except CustomException as _ex:
				await session.rollback()
				raise _ex
	
	except CustomException as _ex:
		print(_ex.detail)
	except Exception as _ex:
		print(_ex)
