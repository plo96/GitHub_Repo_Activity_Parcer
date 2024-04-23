"""
    Функции для парсинга GitHub
"""
from datetime import datetime

import httpx

from src.core.schemas import RepoActivityDTO, RepoDTO
from src.core.models.repos import LIMIT_TOP_REPOS_LIST
from src.project.decorators import multiply_parsing_trying

GH_REST_API_URL_TOP = 'https://api.github.com/search/repositories'


class GithubParserRest:
    
    def __init__(self, github_token: str = None):
        """
        Инициализация объекта GithubParserRest

        :param github_token: токен для аутентификации GitHub API
        """
        self.github_token = github_token
        self.headers = {'Authorization': f'token {self.github_token}'} if self.github_token else {}
    
    @multiply_parsing_trying
    async def parsing_top(self) -> list[RepoDTO] | None:
        """
        Парсинг топа репозиториев по звёздам с гитхаба

        :return: список словарей с указанными в методе данными о репозиториях
        """
        new_top_repos: list = []
        params = {'q': 'stars:>0', 'sort': 'stars', 'order': 'desc', 'per_page': LIMIT_TOP_REPOS_LIST}
        
        # api_keys_model_keys = {
        #     "full_name": "repo",
        #     "owner": "owner",
        #     "stargazers_count": "stars",
        #     "watchers": "watchers",
        #     "forks": "forks",
        #     "open_issues": "open_issues",
        #     "language": "language",
        # }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    url=GH_REST_API_URL_TOP,
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
            # new_repo: dict = {}
            # for api_key, model_key in api_keys_model_keys.items():
            #     new_repo[model_key] = repo[api_key] if api_key != "owner" else repo[api_key]['login']
            new_top_repos.append(new_repo)
        return new_top_repos
    
    @multiply_parsing_trying
    async def parsing_activities(self, repo: dict) -> list[RepoActivityDTO] | None:
        """
        Метод для парсинга активности репозиториев из списка с гитхаба
        
        :param repo: репозиторий для которого мы ищем активности.
        
        :return:
        """
        url = f"https://api.github.com/repos/{repo["repo"]}/commits"
        # params = {"since": "2024-01-01T00:00:00Z", "until": "2024-04-01T00:00:00Z"}
    
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    url=GH_REST_API_URL_TOP,
                    # params=params,
                    headers=self.headers,
                    timeout=5,
                )
            except TimeoutError:
                return
            
            print(response.status_code)
            
            if response.status_code != 200:
                return
            
            response_data = response.json()
            
        list_of_commits: list = []
        for commit in response_data:
            commit_dict = dict(
                name=commit['commit']['author']['name'],
                date=datetime.fromisoformat(commit['commit']['author']['date']).date(),
            )
            
            list_of_commits.append(commit_dict)
        
        repo_activities = RepoActivityDTO.init_from_parsing_data(
            list_of_commits=list_of_commits,
        )
        
        return repo_activities
        