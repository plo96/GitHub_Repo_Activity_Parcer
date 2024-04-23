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

# smth = get_commits_by_date(
#     repo="meta-llama/llama3",
#     start_date="2024-01-01T00:00:00Z",
#     end_date="2024-04-01T00:00:00Z",
#     token=settings.API_KEY,
# )


url = 'https://api.github.com/graphql'

# Задаем заголовок с авторизационным токеном
headers = {
    'Authorization': f'token {settings.API_KEY}',
}

# Задаем строку запроса GraphQL
query = '''
query {
  repository(owner: "meta-llama", name: "llama3") {
    refs(refPrefix: "refs/heads/", first: 100) {
      nodes {
        name
        target {
          ... on Commit {
            history(first: 100, since: "2024-01-01T00:00:00Z", until: "2024-04-01T00:00:00Z") {
              totalCount
              nodes {
                committedDate
                author {
                  name
                  email
                }
              }
            }
          }
        }
      }
    }
  }
}
'''

# Выполняем POST-запрос к эндпоинту GraphQL API GitHub
response = req.post(url, json={'query': query}, headers=headers)

# Печатаем результат запроса
print(response.json())

# graphql request
# {'data': {'repository': {'refs': {'nodes': [{'name': 'gh/HDCharles/1/base', 'target': {'history': {'totalCount': 4, 'nodes': [{'committedDate': '2024-03-26T14:04:40Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T14:03:50Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:56:52Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:53:46Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}]}}}, {'name': 'gh/HDCharles/1/head', 'target': {'history': {'totalCount': 4, 'nodes': [{'committedDate': '2024-03-26T14:04:40Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T14:03:50Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:56:52Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:53:46Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}]}}}, {'name': 'gh/HDCharles/1/orig', 'target': {'history': {'totalCount': 4, 'nodes': [{'committedDate': '2024-03-26T14:04:40Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T14:03:50Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:56:52Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:53:46Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}]}}}, {'name': 'gh/HDCharles/2/base', 'target': {'history': {'totalCount': 4, 'nodes': [{'committedDate': '2024-03-26T14:04:40Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T14:03:50Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:56:52Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:53:46Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}]}}}, {'name': 'gh/HDCharles/2/head', 'target': {'history': {'totalCount': 4, 'nodes': [{'committedDate': '2024-03-26T14:04:40Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T14:03:50Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:56:52Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:53:46Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}]}}}, {'name': 'gh/HDCharles/2/orig', 'target': {'history': {'totalCount': 4, 'nodes': [{'committedDate': '2024-03-26T14:04:40Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T14:03:50Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:56:52Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:53:46Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}]}}}, {'name': 'gh/HDCharles/3/base', 'target': {'history': {'totalCount': 4, 'nodes': [{'committedDate': '2024-03-26T14:04:40Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T14:03:50Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:56:52Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:53:46Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}]}}}, {'name': 'gh/HDCharles/3/head', 'target': {'history': {'totalCount': 4, 'nodes': [{'committedDate': '2024-03-26T14:04:40Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T14:03:50Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:56:52Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:53:46Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}]}}}, {'name': 'gh/HDCharles/3/orig', 'target': {'history': {'totalCount': 4, 'nodes': [{'committedDate': '2024-03-26T14:04:40Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T14:03:50Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:56:52Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:53:46Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}]}}}, {'name': 'gh/HDCharles/4/base', 'target': {'history': {'totalCount': 4, 'nodes': [{'committedDate': '2024-03-26T14:04:40Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T14:03:50Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:56:52Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:53:46Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}]}}}, {'name': 'gh/HDCharles/4/head', 'target': {'history': {'totalCount': 4, 'nodes': [{'committedDate': '2024-03-26T14:04:40Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T14:03:50Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:56:52Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:53:46Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}]}}}, {'name': 'gh/HDCharles/4/orig', 'target': {'history': {'totalCount': 4, 'nodes': [{'committedDate': '2024-03-26T14:04:40Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T14:03:50Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:56:52Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:53:46Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}]}}}, {'name': 'gitkwr-patch-1', 'target': {'history': {'totalCount': 4, 'nodes': [{'committedDate': '2024-03-26T14:04:40Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T14:03:50Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:56:52Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:53:46Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}]}}}, {'name': 'main', 'target': {'history': {'totalCount': 4, 'nodes': [{'committedDate': '2024-03-26T14:04:40Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T14:03:50Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:56:52Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:53:46Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}]}}}, {'name': 'modelnameupdate', 'target': {'history': {'totalCount': 4, 'nodes': [{'committedDate': '2024-03-26T14:04:40Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T14:03:50Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:56:52Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:53:46Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}]}}}, {'name': 'remove7binstances', 'target': {'history': {'totalCount': 4, 'nodes': [{'committedDate': '2024-03-26T14:04:40Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T14:03:50Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:56:52Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:53:46Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}]}}}, {'name': 'special-tokens', 'target': {'history': {'totalCount': 4, 'nodes': [{'committedDate': '2024-03-26T14:04:40Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T14:03:50Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:56:52Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:53:46Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}]}}}, {'name': 'update-examples', 'target': {'history': {'totalCount': 4, 'nodes': [{'committedDate': '2024-03-26T14:04:40Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T14:03:50Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:56:52Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:53:46Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}]}}}, {'name': 'xingjia01-download-script', 'target': {'history': {'totalCount': 4, 'nodes': [{'committedDate': '2024-03-26T14:04:40Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T14:03:50Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:56:52Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}, {'committedDate': '2024-03-26T13:53:46Z', 'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com'}}]}}}]}}}}







#
#
#
# {
#     "url": "https://api.github.com/repos/octocat/Hello-World/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
#     "sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
#     "node_id": "MDY6Q29tbWl0NmRjYjA5YjViNTc4NzVmMzM0ZjYxYWViZWQ2OTVlMmU0MTkzZGI1ZQ==",
#     "html_url": "https://github.com/octocat/Hello-World/commit/6dcb09b5b57875f334f61aebed695e2e4193db5e",
#     "comments_url": "https://api.github.com/repos/octocat/Hello-World/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e/comments",
#     "commit": {
#       "url": "https://api.github.com/repos/octocat/Hello-World/git/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
#       "author":
#         {
#         "name": "Monalisa Octocat",
#         "email": "support@github.com",
#         "date": "2011-04-14T16:00:49Z"
#       },
#       "committer": {
#         "name": "Monalisa Octocat",
#         "email": "support@github.com",
#         "date": "2011-04-14T16:00:49Z"
#       },
#       "message": "Fix all the bugs",
#       "tree": {
#         "url": "https://api.github.com/repos/octocat/Hello-World/tree/6dcb09b5b57875f334f61aebed695e2e4193db5e",
#         "sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e"
#       },
#       "comment_count": 0,
#       "verification": {
#         "verified": false,
#         "reason": "unsigned",
#         "signature": null,
#         "payload": null
#       }
#     },
#     "author": {
#       "login": "octocat",
#       "id": 1,
#       "node_id": "MDQ6VXNlcjE=",
#       "avatar_url": "https://github.com/images/error/octocat_happy.gif",
#       "gravatar_id": "",
#       "url": "https://api.github.com/users/octocat",
#       "html_url": "https://github.com/octocat",
#       "followers_url": "https://api.github.com/users/octocat/followers",
#       "following_url": "https://api.github.com/users/octocat/following{/other_user}",
#       "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
#       "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
#       "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
#       "organizations_url": "https://api.github.com/users/octocat/orgs",
#       "repos_url": "https://api.github.com/users/octocat/repos",
#       "events_url": "https://api.github.com/users/octocat/events{/privacy}",
#       "received_events_url": "https://api.github.com/users/octocat/received_events",
#       "type": "User",
#       "site_admin": false
#     },
#     "committer": {
#       "login": "octocat",
#       "id": 1,
#       "node_id": "MDQ6VXNlcjE=",
#       "avatar_url": "https://github.com/images/error/octocat_happy.gif",
#       "gravatar_id": "",
#       "url": "https://api.github.com/users/octocat",
#       "html_url": "https://github.com/octocat",
#       "followers_url": "https://api.github.com/users/octocat/followers",
#       "following_url": "https://api.github.com/users/octocat/following{/other_user}",
#       "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
#       "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
#       "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
#       "organizations_url": "https://api.github.com/users/octocat/orgs",
#       "repos_url": "https://api.github.com/users/octocat/repos",
#       "events_url": "https://api.github.com/users/octocat/events{/privacy}",
#       "received_events_url": "https://api.github.com/users/octocat/received_events",
#       "type": "User",
#       "site_admin": false
#     },
#     "parents": [
#       {
#         "url": "https://api.github.com/repos/octocat/Hello-World/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e",
#         "sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e"
#       }
#     ]
#   }
# ]
#     {'sha': 'beb213ad429639c5574bbd6323fb4f25c5c606ab',
#      'node_id': 'C_kwDOLg51MdoAKGJlYjIxM2FkNDI5NjM5YzU1NzRiYmQ2MzIzZmI0ZjI1YzVjNjA2YWI',
#      'commit':
#          {
#          'author':
#              {
#                  'name': 'Joseph Spisak',
#                  'email': 'spisakjo@gmail.com',
#                  'date': '2024-03-26T14:04:40Z'
#              },
#              'committer':
#                  {
#                      'name': 'GitHub',
#                      'email': 'noreply@github.com',
#                      'date': '2024-03-26T14:04:40Z'
#                  },
#              'message': 'Update README.md',
#              'tree':
#                  {
#                      'sha': '05ebc09411a0ec311efcdda19cd46e3dc53374e9',
#                      'url': 'https://api.github.com/repos/meta-llama/llama3/git/trees/05ebc09411a0ec311efcdda19cd46e3dc53374e9'
#                  },
#              'url': 'https://api.github.com/repos/meta-llama/llama3/git/commits/beb213ad429639c5574bbd6323fb4f25c5c606ab',
#              'comment_count': 0,
#              'verification':
#                  {
#                      'verified': True,
#                      'reason': 'valid',
#                      'signature': '-----BEGIN PGP SIGNATURE-----\n\nwsFcBAABCAAQBQJmAtX4CRC1aQ7uu5UhlAAAxsYQAHP/QC/WRw/I5jyPO0bg25A3\nr/fFyZY6wbmS/nU/oGQG2goci/JGVaQ3M7+/cAOF3snid77pzWt311V29j2twNmx\n8d4IlpkLUUbfUFkcX0Y6mneCdgzvGOgNoejaRcu2A2hoZMQNkf9y/fFMLuSg61hi\nx0hGPHecb6kPbm71B1mzot5mRfDPIqnVd0jaPiKudXsPpdnnRXYsC4LDQ7aO90JK\n82o0gd4fCbInyBMCfHa6UjjLmDAMpQ0294iH/gM88grV6lvDU/D6Pf2mBSDNqOgq\nrmcffnB3c/m6LRAG/gaFQX32gYp6xYWeUHgZ9P8EUa71Bs5bgvXMgY21Dglnvge1\njgrJ6DhwFyFwtH8qIMOqt1cieQOn3EBLdOUps0+/1cU9ThC0xd7Dwuv7+0oe5RmS\naqk/1lN/MGrHR+4A/o7nOjJVwQn4tXVidITjENmhLZ5eHbVaqrp2FUZifIU7W54S\nzTJPi+heCHlsUNrNiCVD3DaaxwIWa5S2HZHwVyS6qHKTzjnRlePtkJXKqNbScC/n\n5rMYNXErf33KjFre1TTr0/naTDW3UzEgM0Y9sHc8seCldAcUVP5yGFM+M+jMgj0m\n/uJaJcOe/2j0auImUzEHUPtejeyy3mK7Pvtpob/Db+/eD7GSTTbZl47eiFjlv3Wu\nZXipsyq8ytN5Sindq7/Q\n=flI5\n-----END PGP SIGNATURE-----\n', 'payload': 'tree 05ebc09411a0ec311efcdda19cd46e3dc53374e9\nparent d9a94361e57bfaa08b54c3fd76037868dbe088c4\nauthor Joseph Spisak <spisakjo@gmail.com> 1711461880 -0700\ncommitter GitHub <noreply@github.com> 1711461880 -0700\n\nUpdate README.md'
#                  }
#          },
#      'url': 'https://api.github.com/repos/meta-llama/llama3/commits/beb213ad429639c5574bbd6323fb4f25c5c606ab',
#      'html_url': 'https://github.com/meta-llama/llama3/commit/beb213ad429639c5574bbd6323fb4f25c5c606ab',
#      'comments_url': 'https://api.github.com/repos/meta-llama/llama3/commits/beb213ad429639c5574bbd6323fb4f25c5c606ab/comments',
#      'author':
#          {
#              'login': 'jspisak',
#              'id': 11398925,
#              'node_id': 'MDQ6VXNlcjExMzk4OTI1',
#              'avatar_url': 'https://avatars.githubusercontent.com/u/11398925?v=4',
#              'gravatar_id': '',
#              'url': 'https://api.github.com/users/jspisak',
#              'html_url': 'https://github.com/jspisak',
#              'followers_url': 'https://api.github.com/users/jspisak/followers',
#              'following_url': 'https://api.github.com/users/jspisak/following{/other_user}',
#              'gists_url': 'https://api.github.com/users/jspisak/gists{/gist_id}',
#              'starred_url': 'https://api.github.com/users/jspisak/starred{/owner}{/repo}',
#              'subscriptions_url': 'https://api.github.com/users/jspisak/subscriptions',
#              'organizations_url': 'https://api.github.com/users/jspisak/orgs',
#              'repos_url': 'https://api.github.com/users/jspisak/repos',
#              'events_url': 'https://api.github.com/users/jspisak/events{/privacy}',
#              'received_events_url': 'https://api.github.com/users/jspisak/received_events',
#              'type': 'User',
#              'site_admin': False
#          },
#      'committer':
#          {
#              'login': 'web-flow',
#              'id': 19864447,
#              'node_id': 'MDQ6VXNlcjE5ODY0NDQ3',
#              'avatar_url': 'https://avatars.githubusercontent.com/u/19864447?v=4',
#              'gravatar_id': '',
#              'url': 'https://api.github.com/users/web-flow',
#              'html_url': 'https://github.com/web-flow',
#              'followers_url': 'https://api.github.com/users/web-flow/followers',
#              'following_url': 'https://api.github.com/users/web-flow/following{/other_user}',
#              'gists_url': 'https://api.github.com/users/web-flow/gists{/gist_id}',
#              'starred_url': 'https://api.github.com/users/web-flow/starred{/owner}{/repo}',
#              'subscriptions_url': 'https://api.github.com/users/web-flow/subscriptions',
#              'organizations_url': 'https://api.github.com/users/web-flow/orgs',
#              'repos_url': 'https://api.github.com/users/web-flow/repos',
#              'events_url': 'https://api.github.com/users/web-flow/events{/privacy}',
#              'received_events_url': 'https://api.github.com/users/web-flow/received_events',
#              'type': 'User', 'site_admin': False},
#      'parents':
#          [
#              {
#                  'sha': 'd9a94361e57bfaa08b54c3fd76037868dbe088c4',
#                  'url': 'https://api.github.com/repos/meta-llama/llama3/commits/d9a94361e57bfaa08b54c3fd76037868dbe088c4',
#                  'html_url': 'https://github.com/meta-llama/llama3/commit/d9a94361e57bfaa08b54c3fd76037868dbe088c4'}
#          ]
#      },
# [
#     {
#         'sha': 'd9a94361e57bfaa08b54c3fd76037868dbe088c4',
#         'node_id': 'C_kwDOLg51MdoAKGQ5YTk0MzYxZTU3YmZhYTA4YjU0YzNmZDc2MDM3ODY4ZGJlMDg4YzQ',
#         'commit':
#             {
#                 'author':
#                  {
#                      'name': 'Joseph Spisak',
#                      'email': 'spisakjo@gmail.com',
#                      'date': '2024-03-26T14:03:50Z'
#                  },
#                 'committer':
#                     {
#                         'name': 'GitHub',
#                         'email': 'noreply@github.com',
#                         'date': '2024-03-26T14:03:50Z'},
#                 'message': 'Update README.md', 'tree': {'sha': '3f87de7305ea40e8f591f496585085820b0f5ffb', 'url': 'https://api.github.com/repos/meta-llama/llama3/git/trees/3f87de7305ea40e8f591f496585085820b0f5ffb'}, 'url': 'https://api.github.com/repos/meta-llama/llama3/git/commits/d9a94361e57bfaa08b54c3fd76037868dbe088c4', 'comment_count': 0, 'verification': {'verified': True, 'reason': 'valid', 'signature': '-----BEGIN PGP SIGNATURE-----\n\nwsFcBAABCAAQBQJmAtXGCRC1aQ7uu5UhlAAAAVoQAD4RINtFqu9WF/SS07eMhxD6\nX42txuVcFLIY1NCSFTxVleB9wlDWP6gCef/U2yrEODwZZ9IobVTwsRT7GAKdXri+\nDvzsNeJeDId4XCEIoYTdiHOk++Vuj8DqVB/G1uq/iJnBB2TSOjzjAJzG5DujnEH8\nbTYYdJd+lMfV0Xf6nzouSzBIOS94w+vtN6cNLrRU5LDUEtjBt6Y9GL5Pj2TcpinZ\nR6OZkJNsKMy0x/D5NpS2kZcowMUuoYDGpMICBO2TxIF7G0qNGJiZG3HlH/AQ1Ujk\n3Cab9SeLAr5Icd7OUyU4D27rbGrf2cV2Q2Jt6Bi1749WPqDTqr0qEvuruXybwoWN\n5z3LJ3bIICj//KDfUNKnUxZ0czN7UCks1WaEltIjh52ASnr9KIKvNZBqxg4WAdBX\nbHrozo2siCZ10SrKO8tFAkfOLpe8y7uWbA7w21EvxjMve6va/fLwRiiOxiNyfXHu\nDFpB1fHQwR4mRC/ZSDw/UGbne1RK/OxTH4PJ5b/acXe/KP5PvQ8B1gisrZNYA+Ro\nF0HzmYojnPs8RqCLvMroUAjJJULEmYjVZZcnAoypJJ85AK2m92QikGYvhIwRpySq\nKcGtcT0GrilW825QO4IgLRhDy2vPPNKeE3be9BcwGMm25FqFimonX78NFRX531pP\nNRgVW2DzNx7tXb4O2TLa\n=tkUv\n-----END PGP SIGNATURE-----\n', 'payload': 'tree 3f87de7305ea40e8f591f496585085820b0f5ffb\nparent 9a1343878e8275dbb19d13776fce67755e1cb9f1\nauthor Joseph Spisak <spisakjo@gmail.com> 1711461830 -0700\ncommitter GitHub <noreply@github.com> 1711461830 -0700\n\nUpdate README.md'}}, 'url': 'https://api.github.com/repos/meta-llama/llama3/commits/d9a94361e57bfaa08b54c3fd76037868dbe088c4', 'html_url': 'https://github.com/meta-llama/llama3/commit/d9a94361e57bfaa08b54c3fd76037868dbe088c4', 'comments_url': 'https://api.github.com/repos/meta-llama/llama3/commits/d9a94361e57bfaa08b54c3fd76037868dbe088c4/comments', 'author': {'login': 'jspisak', 'id': 11398925, 'node_id': 'MDQ6VXNlcjExMzk4OTI1', 'avatar_url': 'https://avatars.githubusercontent.com/u/11398925?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/jspisak', 'html_url': 'https://github.com/jspisak', 'followers_url': 'https://api.github.com/users/jspisak/followers', 'following_url': 'https://api.github.com/users/jspisak/following{/other_user}', 'gists_url': 'https://api.github.com/users/jspisak/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/jspisak/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/jspisak/subscriptions', 'organizations_url': 'https://api.github.com/users/jspisak/orgs', 'repos_url': 'https://api.github.com/users/jspisak/repos', 'events_url': 'https://api.github.com/users/jspisak/events{/privacy}', 'received_events_url': 'https://api.github.com/users/jspisak/received_events', 'type': 'User', 'site_admin': False}, 'committer': {'login': 'web-flow', 'id': 19864447, 'node_id': 'MDQ6VXNlcjE5ODY0NDQ3', 'avatar_url': 'https://avatars.githubusercontent.com/u/19864447?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/web-flow', 'html_url': 'https://github.com/web-flow', 'followers_url': 'https://api.github.com/users/web-flow/followers', 'following_url': 'https://api.github.com/users/web-flow/following{/other_user}', 'gists_url': 'https://api.github.com/users/web-flow/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/web-flow/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/web-flow/subscriptions', 'organizations_url': 'https://api.github.com/users/web-flow/orgs', 'repos_url': 'https://api.github.com/users/web-flow/repos', 'events_url': 'https://api.github.com/users/web-flow/events{/privacy}', 'received_events_url': 'https://api.github.com/users/web-flow/received_events', 'type': 'User', 'site_admin': False}, 'parents': [{'sha': '9a1343878e8275dbb19d13776fce67755e1cb9f1', 'url': 'https://api.github.com/repos/meta-llama/llama3/commits/9a1343878e8275dbb19d13776fce67755e1cb9f1', 'html_url': 'https://github.com/meta-llama/llama3/commit/9a1343878e8275dbb19d13776fce67755e1cb9f1'}]}, {'sha': '9a1343878e8275dbb19d13776fce67755e1cb9f1', 'node_id': 'C_kwDOLg51MdoAKDlhMTM0Mzg3OGU4Mjc1ZGJiMTlkMTM3NzZmY2U2Nzc1NWUxY2I5ZjE', 'commit': {'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com', 'date': '2024-03-26T13:56:52Z'}, 'committer': {'name': 'GitHub', 'email': 'noreply@github.com', 'date': '2024-03-26T13:56:52Z'}, 'message': 'Update README.md', 'tree': {'sha': '688fd6dd8d29d89c2a70fca76c2aeddc052dc69e', 'url': 'https://api.github.com/repos/meta-llama/llama3/git/trees/688fd6dd8d29d89c2a70fca76c2aeddc052dc69e'}, 'url': 'https://api.github.com/repos/meta-llama/llama3/git/commits/9a1343878e8275dbb19d13776fce67755e1cb9f1', 'comment_count': 0, 'verification': {'verified': True, 'reason': 'valid', 'signature': '-----BEGIN PGP SIGNATURE-----\n\nwsFcBAABCAAQBQJmAtQkCRC1aQ7uu5UhlAAAuugQAF5Ze+xofpNyNcSmg+4T4T3F\n/IvxCJkncgJKyLqQWFIsfqwlrdtoqQegKEP6fcg7sMlFpZraQC3QUZF+XTDFMRCB\nEs6/QU2LrXtzXtquNL+2jEj7rAD9MjwyyJy1A7yoKaTVcAkbGQ98xtu3A/p6nMw3\nbxV/sqTZxuU2cvjF2iMb0e8QBb82Mk1wSagf2dK3tU3eDokxrCcmCYa5XwrPLGWj\nFjBFPE1Gb8fg2Iv40Mrno4zKdPb7d7D7hZXXlXTJ1LlO4DAF+5uWPRZs+vnsGgK8\njjdkV2lxqAoQwH9O/leAUNWZBQJ789t02y09BW8ob9hYk/ySEC9ejgzUBC4J56HT\nEc2JM3yRSSapx/wKvdOvnivfLzdmeE2l7XszTfwZ8iJ+nAeCkX0eMx3V5jRZyviu\nTevxxobYZ71CujKSMQC5kf1F5QrCX+yRm9xbOOlkJyQz9/GST9spO6hoPUIWX5Ng\nJxZO7jYnhEMSo2lXE3hB8Qas8FUAS2oyQScdn91o42Y8pfJ2LN3XDS8z6CDUblIv\nYdyjoNbmpm5kQNVLgePeT8hGbsC6jrbViA8tmjrjNznn2EQ6YY7W4kl/ReD4WxyU\n/QH88HwI3vQnUN9q9dSsI77bomqOXd9V1x14I84utJWADzFT1N9ftcFbu9A3U0mf\nkSxr8N0X/hcDgWR3IlHH\n=GTAp\n-----END PGP SIGNATURE-----\n', 'payload': 'tree 688fd6dd8d29d89c2a70fca76c2aeddc052dc69e\nparent 7931917a3f20ce0875e6246143dc522224c3bed2\nauthor Joseph Spisak <spisakjo@gmail.com> 1711461412 -0700\ncommitter GitHub <noreply@github.com> 1711461412 -0700\n\nUpdate README.md'}}, 'url': 'https://api.github.com/repos/meta-llama/llama3/commits/9a1343878e8275dbb19d13776fce67755e1cb9f1', 'html_url': 'https://github.com/meta-llama/llama3/commit/9a1343878e8275dbb19d13776fce67755e1cb9f1', 'comments_url': 'https://api.github.com/repos/meta-llama/llama3/commits/9a1343878e8275dbb19d13776fce67755e1cb9f1/comments', 'author': {'login': 'jspisak', 'id': 11398925, 'node_id': 'MDQ6VXNlcjExMzk4OTI1', 'avatar_url': 'https://avatars.githubusercontent.com/u/11398925?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/jspisak', 'html_url': 'https://github.com/jspisak', 'followers_url': 'https://api.github.com/users/jspisak/followers', 'following_url': 'https://api.github.com/users/jspisak/following{/other_user}', 'gists_url': 'https://api.github.com/users/jspisak/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/jspisak/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/jspisak/subscriptions', 'organizations_url': 'https://api.github.com/users/jspisak/orgs', 'repos_url': 'https://api.github.com/users/jspisak/repos', 'events_url': 'https://api.github.com/users/jspisak/events{/privacy}', 'received_events_url': 'https://api.github.com/users/jspisak/received_events', 'type': 'User', 'site_admin': False}, 'committer': {'login': 'web-flow', 'id': 19864447, 'node_id': 'MDQ6VXNlcjE5ODY0NDQ3', 'avatar_url': 'https://avatars.githubusercontent.com/u/19864447?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/web-flow', 'html_url': 'https://github.com/web-flow', 'followers_url': 'https://api.github.com/users/web-flow/followers', 'following_url': 'https://api.github.com/users/web-flow/following{/other_user}', 'gists_url': 'https://api.github.com/users/web-flow/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/web-flow/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/web-flow/subscriptions', 'organizations_url': 'https://api.github.com/users/web-flow/orgs', 'repos_url': 'https://api.github.com/users/web-flow/repos', 'events_url': 'https://api.github.com/users/web-flow/events{/privacy}', 'received_events_url': 'https://api.github.com/users/web-flow/received_events', 'type': 'User', 'site_admin': False}, 'parents': [{'sha': '7931917a3f20ce0875e6246143dc522224c3bed2', 'url': 'https://api.github.com/repos/meta-llama/llama3/commits/7931917a3f20ce0875e6246143dc522224c3bed2', 'html_url': 'https://github.com/meta-llama/llama3/commit/7931917a3f20ce0875e6246143dc522224c3bed2'}]}, {'sha': '7931917a3f20ce0875e6246143dc522224c3bed2', 'node_id': 'C_kwDOLg51MdoAKDc5MzE5MTdhM2YyMGNlMDg3NWU2MjQ2MTQzZGM1MjIyMjRjM2JlZDI', 'commit': {'author': {'name': 'Joseph Spisak', 'email': 'spisakjo@gmail.com', 'date': '2024-03-26T13:53:46Z'}, 'committer': {'name': 'GitHub', 'email': 'noreply@github.com', 'date': '2024-03-26T13:53:46Z'}, 'message': 'Create README.md', 'tree': {'sha': '7942bd096416def127cfff0d06741c5a3587f621', 'url': 'https://api.github.com/repos/meta-llama/llama3/git/trees/7942bd096416def127cfff0d06741c5a3587f621'}, 'url': 'https://api.github.com/repos/meta-llama/llama3/git/commits/7931917a3f20ce0875e6246143dc522224c3bed2', 'comment_count': 0, 'verification': {'verified': True, 'reason': 'valid', 'signature': '-----BEGIN PGP SIGNATURE-----\n\nwsFcBAABCAAQBQJmAtNqCRC1aQ7uu5UhlAAAmTQQAAA6HmRfzDd1YJiyx89aDdmv\n3RPEcAOgXO9WoztNG1EnssWcJSnjETPeo+YbT1Qgf3E5ND7ytx+tqVDCGtHM/VL/\nPLE76T4idBIgnvR3EeIV2ZeTUfLufoJIGjUNf0tnHh+KJYvk8QGAv1vqQ1+OFrDu\nueXRK4XZbf++6yw9ZfdNOrE4hcC9prfCUv24RvFgjTs8pdOx3Yu0vtPwH0jpnG4X\nf+AxuWgv+jv2vz4TxppE57j9tT35ByeMiSGK4UXuZnIksw7LgARf45HOMpy+i56M\n/cEnzRbJaTmICuszbeuCy26cdCS3Tw8u+pgph3sMIrwSTtgioY/6W4kovF540eZu\nNoBBrKSXVstc7n+N3YOlU84uEvDb6nMQq9Mog3MxD3I8pGi/eIWk/qUAjAeJ8ggm\neGXUTi1P4MROFQ8nI1tPvGg04eqNVgSksd6aIW7ipUPGrPDKHrEhzik1K56/jqLE\nko0tHtn1SCVrMBNoGSjxYszMfS2ij9hQSjKPN6AV89TbEQ9ubipJlR2Hxdypr4Fg\nxU6aJj53CLOvHkF5KIhEzH/qnznCTaEuqTFpZY6H+dqVY1mBG8QMLPKoSjspqsrK\nG8dJnXlBRdutT7/64ZVyocIFNmzmZQgLwUSqkzks/yNhi2X1cW4r7DQmH+g48kD8\njt1vIJuca+bMpMwS+eCg\n=Cxfu\n-----END PGP SIGNATURE-----\n', 'payload': 'tree 7942bd096416def127cfff0d06741c5a3587f621\nauthor Joseph Spisak <spisakjo@gmail.com> 1711461226 -0700\ncommitter GitHub <noreply@github.com> 1711461226 -0700\n\nCreate README.md'}}, 'url': 'https://api.github.com/repos/meta-llama/llama3/commits/7931917a3f20ce0875e6246143dc522224c3bed2', 'html_url': 'https://github.com/meta-llama/llama3/commit/7931917a3f20ce0875e6246143dc522224c3bed2', 'comments_url': 'https://api.github.com/repos/meta-llama/llama3/commits/7931917a3f20ce0875e6246143dc522224c3bed2/comments', 'author': {'login': 'jspisak', 'id': 11398925, 'node_id': 'MDQ6VXNlcjExMzk4OTI1', 'avatar_url': 'https://avatars.githubusercontent.com/u/11398925?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/jspisak', 'html_url': 'https://github.com/jspisak', 'followers_url': 'https://api.github.com/users/jspisak/followers', 'following_url': 'https://api.github.com/users/jspisak/following{/other_user}', 'gists_url': 'https://api.github.com/users/jspisak/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/jspisak/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/jspisak/subscriptions', 'organizations_url': 'https://api.github.com/users/jspisak/orgs', 'repos_url': 'https://api.github.com/users/jspisak/repos', 'events_url': 'https://api.github.com/users/jspisak/events{/privacy}', 'received_events_url': 'https://api.github.com/users/jspisak/received_events', 'type': 'User', 'site_admin': False}, 'committer': {'login': 'web-flow', 'id': 19864447, 'node_id': 'MDQ6VXNlcjE5ODY0NDQ3', 'avatar_url': 'https://avatars.githubusercontent.com/u/19864447?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/web-flow', 'html_url': 'https://github.com/web-flow', 'followers_url': 'https://api.github.com/users/web-flow/followers', 'following_url': 'https://api.github.com/users/web-flow/following{/other_user}', 'gists_url': 'https://api.github.com/users/web-flow/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/web-flow/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/web-flow/subscriptions', 'organizations_url': 'https://api.github.com/users/web-flow/orgs', 'repos_url': 'https://api.github.com/users/web-flow/repos', 'events_url': 'https://api.github.com/users/web-flow/events{/privacy}', 'received_events_url': 'https://api.github.com/users/web-flow/received_events', 'type': 'User', 'site_admin': False}, 'parents': []}]
