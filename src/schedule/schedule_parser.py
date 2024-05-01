"""
    Настройка задачи парсинга по расписанию.
"""
from asyncio import sleep as asleep

from sqlalchemy.ext.asyncio import async_sessionmaker

from src.project.exceptions import CustomException, TooFewRepos
from src.project.config import settings
from src.core.dependencies import get_actual_session_factory
from src.core.schemas import RepoDTO, RepoActivityDTO, RepoParsing, RepoActivityParsing
from src.parsing import GithubParser, gh_parser
from src.layers.services import RepoService, RepoActivitiesService

DEFAULT_PAUSE_VALUE = 2  # Время паузы между запросами, секунды
FORCED_PREVENTIVES_PARSING = settings.FORCED_PREVENTIVES_PARSING  # Необходимость первоначального парсинга GitHub


class ScheduleParser:
    def __init__(
            self,
            parser: GithubParser,
            session_factory: async_sessionmaker,
            pause_value: int = DEFAULT_PAUSE_VALUE,
            forced_preventives_parsing: bool = FORCED_PREVENTIVES_PARSING,
    ):
        """
        Инициализация объекта парсинга GitHub по расписанию.
        :param parser: Объект парсера GitHub.
        :param session_factory: Фабрика сессий для доступа к актуальной БД.
        :param pause_value: Длительность паузы между запросами, в секундах.
		:param forced_prevetnious_parsing: Параметр для .env для возможности включить принудительный
	   		   первоначальный парсинг (может быть полезно, если программа запускалась давно последний раз)
        """
        self._gh_parser = parser
        self._session_factory = session_factory
        self._pause_value = pause_value
        self._forced_preventives_parsing = forced_preventives_parsing

    async def preventious_full_task_processing(self) -> None:
        """
        Запуск процесса парсинга GitHub если в базе данных недостаточно информации по репозиториям.
        :return: None.
        """
        if self._forced_preventives_parsing:
            await self.full_task_processing()
        else:
            try:
                async with self._session_factory() as session:
                    await RepoService.get_top_repos(
                        session=session,
                    )
            except TooFewRepos:
                await self.full_task_processing()

    async def full_task_processing(self) -> None:
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
    ) -> tuple[list[RepoParsing], list[list[RepoActivityParsing]]]:
        """
        Парсинг GitHub по расписанию для получения данных по топу репозиториев и их активностям.
        :return: Полученные в результате парсинга данные по новому топу репозиториев
                 и активностям по ним за каждый день.
                 Текстовый вывод деталей ошибок в случае их возникновения, без прерывания работы программы.
        """
        try:
            new_top_repos = await self._gh_parser.parsing_top()

            new_repos_activities: list = []
            for repo in new_top_repos:
                await asleep(self._pause_value)
                new_repos_activities.append(
                    await self._gh_parser.parsing_activities(
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
            new_top_repos: list[RepoParsing],
            new_repos_activities: list[list[RepoActivityParsing]],
    ) -> None:
        """
        Запись данных, полученных в результате парсинга, в базу данных.
        :param new_top_repos: Список ДТО-объектов репозиториев нового топа.
        :param new_repos_activities: Список для каждого репозитория, внутри которого
                                     список по дням активностей в данном репозитории GitHub.
        :return: None.
                 Текстовый вывод деталей ошибок в случае их возникновения, без прерывания работы программы.
        """
        async with self._session_factory() as session:
            try:
                new_top_repos: list[RepoDTO] = await RepoService.set_new_top_repos(
                    session=session,
                    new_top_repos=new_top_repos,
                )

                new_repos_activities_dto: list[list[RepoActivityDTO]] = []
                for repo, activities_list in zip(new_top_repos, new_repos_activities):
                    activities_list_dto: list[RepoActivityDTO] = []
                    for activity in activities_list:
                        activity_dict = activity.model_dump()
                        activity_dict.__setitem__("repo_id", repo.id)
                        activities_list_dto.append(RepoActivityDTO.model_validate(activity_dict))
                    new_repos_activities_dto.append(activities_list_dto)

                await RepoActivitiesService.set_new_repo_activities(
                    session=session,
                    new_repos_activities=new_repos_activities_dto,
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
