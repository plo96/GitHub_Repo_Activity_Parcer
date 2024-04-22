"""
    Функции для парсинга GitHub
"""
import httpx

from src.core.models.repos import LIMIT_TOP_REPOS_LIST
from src.project.decorators import multiply_parsing_trying

GH_REST_API_URL_TOP = 'https://api.github.com/search/repositories'


class GithubParser:
    
    def __init__(self, github_token: str = None):
        self.github_token = github_token
    
    @multiply_parsing_trying
    async def parsing_top_rest_api(self) -> list[dict] | None:
        """Метод для парсинга топа репозиториев по звёздам с гитхаба"""
        new_top_repos: list = []
        params = {'q': 'stars:>0', 'sort': 'stars', 'order': 'desc', 'per_page': LIMIT_TOP_REPOS_LIST}
        headers = {'Authorization': f'token {self.github_token}'} if self.github_token else {}
        
        api_keys_model_keys = {
            "full_name": "repo",
            "owner": "owner",
            "stargazers_count": "stars",
            "watchers": "watchers",
            "forks": "forks",
            "open_issues": "open_issues",
            "language": "language",
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    url=GH_REST_API_URL_TOP,
                    params=params,
                    headers=headers,
                    timeout=5,
                )
            except TimeoutError:
                return
            
            if response.status_code != 200:
                return
            
            response_data = response.json()["items"]
        
        for repo in response_data:
            new_repo: dict = {}
            for api_key, model_key in api_keys_model_keys.items():
                new_repo[model_key] = repo[api_key] if api_key != "owner" else repo[api_key]['login']
            new_top_repos.append(new_repo)
        return new_top_repos
    
    @multiply_parsing_trying
    async def parsing_activities_rest_api(self, list_of_repos: list[dict]) -> list[list[dict]] | None:
        """Метод для парсинга активности репозиториев из списка с гитхаба"""
        ...
        