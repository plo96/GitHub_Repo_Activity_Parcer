import requests as req

from src.project.config import settings

GITHUB_TOKEN = settings.API_KEY

GH_REST_API_URL = 'https://api.github.com/search/repositories'
params = {'q': 'stars:>0', 'sort': 'stars', 'order': 'desc', 'per_page': 5}
headers = {'Authorization': f'token {GITHUB_TOKEN}'}

response = req.get(url=GH_REST_API_URL, params=params, headers=headers)

repo_dict: dict = response.json()['items'][0]
insteresting_keys = (
    "full_name",
    "owner",
    "stargazers_count",
    "watchers",
    "forks",
    "open_issues",
    "language",
)



for key in insteresting_keys:
    if key == "owner":
        print(f"{repo_dict[key]['login']=}")
    else:
        print(f"{repo_dict[key]=}")

import httpx


async def parse_github_data():
    async with httpx.AsyncClient() as client:
        url = 'https://api.github.com/search/repositories?q=stars:>0&sort=stars&order=desc'
        response = await client.get(url)
        data = response.json()

        # Здесь вы можете распарсить данные и выполнить необходимую обработку
        # Например, вывести их на экран или сохранить в базу данных
        for repo in data['items']:
            print(repo['name'], repo['owner']['login'], repo['stargazers_count'])

            import aioschedule
            import asyncio

            # Запланируйте выполнен ие функции каждый день в определенное время
            aioschedule.every().day.at("10:00").do(parse_github_data)

            # Запускайте планировщик задач в фоновом режиме
            async def background_task():
                while True:
                    await aioschedule.run_pending()
                    await asyncio.sleep(60)  # Подождите 60 секунд перед следующей проверкой расписания

            # Запустите фоновую задачу
            async def main():
                await background_task()

            # Запустите ваше асинхронное приложение FastAPI
            if __name__ == "__main__":
                asyncio.run(main())




import asyncio
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Инициализируем FastAPI приложение
app = FastAPI()

# Создаем планировщик задач
scheduler = AsyncIOScheduler()

# Асинхронная задача, которую мы будем выполнять по расписанию
async def scheduled_task():
    print("Running scheduled task...")
    # Здесь можно выполнять любую асинхронную работу
    # Например, выполнение запросов к API, обработка данных и т. д.

# Запускаем асинхронную задачу по расписанию
# scheduler.add_job(scheduled_task, trigger='interval', seconds=10)
# Запускаем асинхронную задачу по расписанию
scheduler.add_job(scheduled_task, trigger='cron', hour=10, minute=0)

# Запускаем планировщик задач
scheduler.start()

# Запускаем приложение
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)