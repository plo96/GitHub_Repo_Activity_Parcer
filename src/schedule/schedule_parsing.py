"""
	Настройка задачи парсинга по расписанию.
"""
from asyncio import sleep as asleep

from fastapi_utilities import repeat_at

from src.project import settings
from src.project.exceptions import CustomException
from src.parsing.github import GithubParserRest
from src.layers.services import RepoService, RepoActivitiesService
from src.core.dependencies import get_actual_session_factory


@repeat_at(cron="0 7 * * *")
async def schedule_parsing() -> None:
	"""
	Переодическая функция для парсинга данных с GitHub и последующей их записи в базу данных приложения.
	:return: None. Текстовый вывод деталей ошибок в случае их возникновения, без прерывания работы программы.
	"""
	try:
		print("Start parsing.")
		gh_parser = GithubParserRest(settings.API_KEY)
		
		new_top_repos = await gh_parser.parsing_top()
		
		new_repos_activities: list = []
		for repo in new_top_repos:
			await asleep(2)
			new_repos_activities.append(
				await gh_parser.parsing_activities(
					repo=repo,
				)
			)
		
		print('Parsing is done.')
		
		session_factory = get_actual_session_factory()
		async with session_factory() as session:
			
			try:
				await RepoService.set_new_top_repos(
					session=session,
					new_top_repos=new_top_repos,
				)
			
				for repo, activities_list in zip(new_top_repos, new_repos_activities):
					for activity in activities_list:
						activity.__setattr__("repo_id", repo.id)
				
				await RepoActivitiesService.set_new_repo_activities(
					session=session,
					new_repos_activities=new_repos_activities,
				)
			
				await session.commit()
			except CustomException as _ex:
				await session.rollback()
				raise _ex
			
		print('DB changes are commited.')
	except CustomException as _ex:
		print(_ex.detail)
	except Exception as _ex:
		print(_ex)
