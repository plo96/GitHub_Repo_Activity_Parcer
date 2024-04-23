import requests as req

from src.project import settings


def get_commits_by_date(repo: str, start_date: str, end_date: str, token: str) -> list:
	url = f"https://api.github.com/repos/{repo}/commits"
	params = {"since": start_date, "until": end_date}
	headers = {"Authorization": f"token {token}"}
	response = req.get(url, params=params, headers=headers)
	commits = response.json()
	
	print(commits)
	
	commit_details = [(commit["commit"]["author"]["name"], commit["commit"]["author"]["date"]) for commit in commits]
	return commit_details


# Пример использования

smth = get_commits_by_date(
    repo="public-apis/public-apis",
    # repo="meta-llama/llama3",
    start_date="2024-01-01T00:00:00Z",
    end_date="2024-04-01T00:00:00Z",
    token=settings.API_KEY,
)

print(smth)

# url = 'https://api.github.com/graphql'
#
# # Задаем заголовок с авторизационным токеном
# headers = {
# 	'Authorization': f'token {settings.API_KEY}',
# }

# Задаем строку запроса GraphQL
# query = '''
# query {
#   repository(owner: "meta-llama", name: "llama3") {
#     refs(refPrefix: "refs/heads/", first: 100) {
#       nodes {
#         name
#         target {
#           ... on Commit {
#             history(first: 100, since: "2024-01-01T00:00:00Z", until: "2024-04-01T00:00:00Z") {
#               totalCount
#               nodes {
#                 committedDate
#                 author {
#                   name
#                   email
#                 }
#               }
#             }
#           }
#         }
#       }
#     }
#   }
# }
# '''

# Выполняем POST-запрос к эндпоинту GraphQL API GitHub
# response = req.post(url, json={'query': query}, headers=headers)

# Печатаем результат запроса
# print(response.json())
