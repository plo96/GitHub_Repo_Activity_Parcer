"""
    Класс для реализации парсинга GitHub с использованием его RestAPI.
"""
from abc import ABC, abstractmethod
from datetime import datetime

import httpx

from src.core.schemas import RepoActivityParsing, RepoParsing
from src.core.models.repos import LIMIT_TOP_REPOS_LIST
from src.project.decorators import multiply_parsing_trying
from src.project import settings

MAX_PARSING_TRYING = 5      # Максимальное число попыток в случае неудачи при парсинге.


class GithubParser(ABC):
    """Базовый класс для реализации парсера GitHub."""

    @abstractmethod
    async def parsing_top(
            self,
    ) -> list[RepoParsing] | None:
        """
		Парсинг топа репозиториев по звёздам с гитхаба.
        :return: Список словарей с указанными в методе данными о репозиториях.
                 None в случае неудачного запроса.
		"""
        ...

    @abstractmethod
    async def parsing_activities(
            self,
            repo: RepoParsing,
    ) -> list[RepoActivityParsing] | None:
        """
		Парсинг активности одного репозитория GitHub.
        :param repo: Репозиторий для которого мы ищем активности.
        :return: Список ДТО-схем для активности репозитория.
		"""
        ...


class GithubParserRest(GithubParser):
    """Класс для реализации парсинга GitHub через его RestAPI."""

    def __init__(self, github_token: str = None):
        """
        Инициализация объекта GithubParserRest.
        :param github_token: Токен для аутентификации при взаимодействии с  GitHub API.
        """
        self.github_token = github_token
        self.headers = {'Authorization': f'token {self.github_token}'} if self.github_token else {}

    @multiply_parsing_trying(MAX_PARSING_TRYING)
    async def parsing_top(
            self,
    ) -> list[RepoParsing] | None:
        """
        Реализация парсинга топа репозиториев через RestAPI.
        :return: Список словарей с указанными в методе данными о репозиториях.
                 None в случае неудачного запроса.
        """
        url: str = 'https://api.github.com/search/repositories'
        params: dict = {
            'q': 'stars:>0',
            'sort': 'stars',
            'order': 'desc',
            'per_page': LIMIT_TOP_REPOS_LIST
        }

        new_top_repos: list = []
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url=url,
                    params=params,
                    headers=self.headers,
                    timeout=5,
                )
                if response.status_code != 200:
                    return
                response_data = response.json()["items"]

            for index, repo in enumerate(response_data):
                new_top_repos.append(
                    RepoParsing(
                        repo=repo.get("name"),
                        owner=repo.get("owner").get("login"),
                        stars=repo.get("stargazers_count"),
                        watchers=repo.get("watchers"),
                        forks=repo.get("forks"),
                        open_issues=repo.get("open_issues"),
                        language=repo.get("language"),
                        position_cur=index,
                    )
                )
            return new_top_repos
        except Exception as _ex:
            print(_ex)
            return

    @multiply_parsing_trying(MAX_PARSING_TRYING)
    async def parsing_activities(
            self,
            repo: RepoParsing,
    ) -> list[RepoActivityParsing] | None:
        """
        Парсинг активности одного репозитория GitHub через RestAPI.
        :param repo: Репозиторий для которого мы ищем активности.
        :return: Список ДТО-схем для активности репозитория.
        """
        url: str = f"https://api.github.com/repos/{repo.owner}/{repo.repo}/commits"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url=url,
                    headers=self.headers,
                    timeout=5,
                )
                if response.status_code != 200:
                    return
                response_data = response.json()

            list_of_commits: list = []
            for commit in response_data:
                commit_dict = dict(
                    name=commit['commit']['author']['name'],
                    date=datetime.strptime(commit['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ").date(),
                )
                list_of_commits.append(commit_dict)

            repo_activities = RepoActivityParsing.validate_from_parsing_data(
                list_of_commits=list_of_commits,
            )

            return repo_activities
        except Exception as _ex:
            print(_ex)
            return


gh_parser = GithubParserRest(settings.API_KEY)
