"""
    Основной файл приложения:
    - Инициализация приложения;
    - Подключение роутеров;
    - Настройка жизненного цикла, подключение задач по расписанию;
    - Настройка и подключение middleware;
    - Запуск приложения через uvicorn.
"""
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
from time import time

from fastapi import FastAPI, Request
import uvicorn

from src.project.decorators import router_exceptions_processing
from src.layers.routers import router
# from src.schedule import schedule_parsing

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def init_scheduler():
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(some_task)
    # scheduler.start()
    async_scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    await some_task()
    async_scheduler.add_job(some_task, trigger="interval", days=1)
    async_scheduler.start()


async def some_task():
    print('hi start')
    await asyncio.sleep(5)
    print('hi stop')


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    """'Обертка' для реализации событий до и после запуска приложения"""
    print('Server starts')
    await init_scheduler()
    # await schedule_parsing()
    yield
    print('Server stops')


app = FastAPI(
    title="GH_TestTask",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router, prefix="/api")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Настройка middleware.
    :param request: Параметры входящего запроса.
    :param call_next: Функция формирования ответа.
    :return: Ответ от сервера.
    """
    start_time = time()
    response = await call_next(request)
    process_time = time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get('/')
@router_exceptions_processing
async def say_hello():
    """Тестовое сообщение для проверки работоспособности приложения"""
    return 'Hello!'


if __name__ == '__main__':
    uvicorn.run(app, reload=False)
