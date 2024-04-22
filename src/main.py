from contextlib import asynccontextmanager
from time import time
import asyncio

from fastapi import FastAPI, Request
import uvicorn

from src.project.exceptions import exceptions_processing
from src.layers.routers import router

from fastapi_utilities import repeat_at


@repeat_at(cron="0 0 * * *")
async def print_hello():
    print("Starting schedule job...")
    await asyncio.sleep(5)
    print("Schedule job is done!")


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    """'Обертка' для реализации событий до и после запуска приложения"""
    print('Server starts')

    await print_hello()
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
    start_time = time()
    response = await call_next(request)
    process_time = time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get('/')
@exceptions_processing
async def say_hello():
    """Тестовое сообщение для проверки работоспособности приложения"""
    return 'Hello!'


if __name__ == '__main__':
    uvicorn.run(app, reload=False)


# * * * * * *
# | | | | | |
# | | | | | +-- Year              (range: 1900-3000)
# | | | | +---- Day of the Week   (range: 1-7, 1 standing for Monday)
# | | | +------ Month of the Year (range: 1-12)
# | | +-------- Day of the Month  (range: 1-31)
# | +---------- Hour              (range: 0-23)
# +------------ Minute            (range: 0-59)

