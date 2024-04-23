"""
    Функции для парсинга GitHub
"""
from datetime import datetime

import httpx

from src.core.schemas import RepoActivityDTO, RepoDTO
from src.core.models.repos import LIMIT_TOP_REPOS_LIST
from src.project.decorators import multiply_parsing_trying


class GithubParserRest:
    
    def __init__(self, github_token: str = None):
        """
        Инициализация объекта GithubParserRest, служащего для парсинга GitHub с использованием его REST API.
        :param github_token: токен для аутентификации GitHub API.
        """
        self.github_token = github_token
        self.headers = {'Authorization': f'token {self.github_token}'} if self.github_token else {}
    
    @multiply_parsing_trying
    async def parsing_top(self) -> list[RepoDTO] | None:
        """
        Парсинг топа репозиториев по звёздам с гитхаба.
        :return: Список словарей с указанными в методе данными о репозиториях или None в случае неудачного запроса.
        """
        url = 'https://api.github.com/search/repositories'
        params = {'q': 'stars:>0', 'sort': 'stars', 'order': 'desc', 'per_page': LIMIT_TOP_REPOS_LIST}

        new_top_repos: list = []
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    url=url,
                    params=params,
                    headers=self.headers,
                    timeout=5,
                )
            except TimeoutError:
                return
            
            if response.status_code != 200:
                return
            
            response_data = response.json()["items"]
        
        for index, repo in enumerate(response_data):
            new_repo = RepoDTO(
                id=None,
                repo=repo.get("full_name"),
                owner=repo.get("owner").get("login"),
                stars=repo.get("stargazers_count"),
                watchers=repo.get("watchers"),
                forks=repo.get("forks"),
                open_issues=repo.get("open_issues"),
                language=repo.get("language"),
                position_cur=index,
                position_prev=None,
            )
            new_top_repos.append(new_repo)
        return new_top_repos
    
    @multiply_parsing_trying
    async def parsing_activities(self, repo: RepoDTO) -> list[RepoActivityDTO] | None:
        """
        Метод для парсинга активности репозиториев из списка с гитхаба.
        :param repo: репозиторий для которого мы ищем активности.
        :return: список ДТО для активности репозиториев.
        """
        url = f"https://api.github.com/repos/{repo.repo}/commits"
    
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    url=url,
                    headers=self.headers,
                    timeout=5,
                )
            except TimeoutError:
                return
            
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
        
        repo_activities = RepoActivityDTO.init_from_parsing_data(
            list_of_commits=list_of_commits,
        )
        
        return repo_activities
        