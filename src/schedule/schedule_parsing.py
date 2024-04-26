"""
	Настройка задачи парсинга по расписанию.
"""
from asyncio import sleep as asleep

from sqlalchemy.ext.asyncio import async_sessionmaker

from src.core.schemas import RepoDTO, RepoActivityDTO
from src.project.exceptions import CustomException
from src.parsing import GithubParser, gh_parser
from src.layers.services import RepoService, RepoActivitiesService
from src.core.dependencies import get_actual_session_factory


class ScheduleParser:
	def __init__(
			self,
			parser: GithubParser,
			session_factory: async_sessionmaker,
	):
		"""
		Инициализация объекта парсинга GitHub по расписанию.
		:param parser: Объект парсера GitHub.
		:param session_factory: Фабрика сессий для доступа к актуальной БД.
		"""
		self.gh_parser = parser
		self.session_factory = session_factory
	
	async def task_processing(self) -> None:
		"""
		Переодическая функция для парсинга данных с GitHub и последующей их записи в базу данных приложения.
		:return: None.
		"""
		print("Start parsing.")
		new_top_repos, new_repos_activities = await self.parsing()
		print('Parsing is done.')
		await self.update_db(new_top_repos, new_repos_activities)
		print('DB changes are committed.')
	
	async def parsing(
			self,
	) -> tuple[list[RepoDTO], list[list[RepoActivityDTO]]]:
		"""
		Парсинг GitHub по расписанию для получения данных по топу репозиториев и их активностям.
		:return: Полученные в результате парсинга данные по новому топу репозиториев
				 и активностям по ним за каждый день.
				 Текстовый вывод деталей ошибок в случае их возникновения, без прерывания работы программы.
		"""
		try:
			new_top_repos = await gh_parser.parsing_top()
			
			new_repos_activities: list = []
			for repo in new_top_repos:
				await asleep(2)
				new_repos_activities.append(
					await self.gh_parser.parsing_activities(
						repo=repo,
					)
				)
			
			return new_top_repos, new_repos_activities
		except CustomException as _ex:
			print(_ex.detail)
		except Exception as _ex:
			print(_ex)
	
	async def update_db(
			self,
			new_top_repos: list[RepoDTO],
			new_repos_activities: list[list[RepoActivityDTO]],
	) -> None:
		"""
		Запись данных, полученных в результате парсинга, в базу данных.
		:param new_top_repos: Список ДТО-объектов репозиториев нового топа.
		:param new_repos_activities: Список для каждого репозитория, внутри которого
		 							 список по дням активностей в данном репозитории GitHub.
		:return: None.
				 Текстовый вывод деталей ошибок в случае их возникновения, без прерывания работы программы.
		"""
		async with self.session_factory() as session:
			try:
				new_top_repos = await RepoService.set_new_top_repos(
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
				print(_ex)
			except Exception as _ex:
				await session.rollback()
				print(_ex)
				
				
schedule_parser = ScheduleParser(
	parser=gh_parser,
	session_factory=get_actual_session_factory(),
)
