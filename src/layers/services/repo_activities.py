"""
	Сервис для осуществления бизнес-логики при работе с активностями репозиториев.
"""
from datetime import datetime, date, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schemas import RepoActivityUpload, RepoActivityDTO
from src.layers.repositories import RepoActivitiesRepository, ReposRepository
from src.project.exceptions import NoRepoActivities, NoRepoOwnerCombination, AddNewDataError


class RepoActivitiesService:
    """
    Класс сервиса для осуществления бизнес-логики при работе с активностями репозиториев.
	Используются статические методы. Экземпляр класса не создаётся.
	"""

    @staticmethod
    async def get_activity(
            session: AsyncSession,
            owner: str,
            repo: str,
            since: date | None,
            until: date | None,
    ) -> list[RepoActivityUpload]:
        """
		Получение информации об активности в конкретном репозитории по дням за определённый промежуток времени.
		Метод для ответа по API.
		:param session: Сессия для доступа к БД.
		:param owner: Имя владельца репозитория на GitHub.
		:param repo: full_name репозитория на GitHub.
		:param since: Начальная точка по времени для выборки.
		:param until: Конечная точка по времени для выборки.
		:return: Список моделей с активностями данного репозитория по дням в пределах запрашиваемого периода.
				 Вызов ошибки из класса CustomHTTPException в случае ошибок.
		"""
        if not since:
            res = await RepoActivitiesRepository.get_min_activity_date(
                session=session,
            )
            if not res:
                raise NoRepoActivities
            since = (res._tuple()[0])       # noqa
        if not until:
            res = await RepoActivitiesRepository.get_max_activity_date(
                session=session,
            )
            if not res:
                raise NoRepoActivities
            until = (res._tuple()[0])      # noqa

        until = until + timedelta(days=1)  # Потому что SQL(по крайней мере sqlite) считает "date":00-00 > "date"
        result = await RepoActivitiesRepository.get_repo_activities(
            session=session,
            owner=owner,
            repo=repo,
            since=since,
            until=until,
        )

        if not result:
            if await ReposRepository.check_owner_repo_combination(
                    session=session,
                    owner=owner,
                    repo=repo,
            ):
                raise NoRepoActivities
            else:
                raise NoRepoOwnerCombination

        repo_activities_upload: list[RepoActivityUpload] = []
        for activity in result:
            activity = activity._asdict()  # noqa
            activity.pop("repo_id")
            activity.__setitem__("date", activity["date"])
            activity.__setitem__("authors", list(activity['authors'].split(", ")))
            repo_activities_upload.append(RepoActivityUpload.model_validate(activity))

        return repo_activities_upload

    @staticmethod
    async def set_new_repo_activities(
            session: AsyncSession,
            new_repos_activities: list[list[RepoActivityDTO]],
    ) -> None:
        """
		Добавление нового списка активностей репозиториев в БД.
		Метод для вызова из периодической задачи.
		:param session: Сессия для доступа к БД.
		:param new_repos_activities: Список со списками активностей для каждого репозитория.
		:return: None.
				 Вызов ошибки AddNewDataError в случае возникновения ошибки.
		"""

        try:
            await RepoActivitiesRepository.delete_all_activities(
                session=session,
            )

            for repo_activities in new_repos_activities:
                for repo_activity in repo_activities:
                    repo_activity_dict = repo_activity.model_dump()
                    repo_activity_dict["authors"] = ", ".join(author for author in repo_activity_dict["authors"])
                    repo_activity_dict["authors"] = repo_activity_dict["authors"].replace("'", "''")
                    await RepoActivitiesRepository.add_activity(
                        session=session,
                        repo_activity_dict=repo_activity_dict,
                    )
        except Exception as _ex:
            print(_ex)
            raise AddNewDataError
