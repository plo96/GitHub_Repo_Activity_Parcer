from contextlib import asynccontextmanager
from time import time

from fastapi import FastAPI, Request
import uvicorn

from src.project.decorators import router_exceptions_processing
from src.layers.routers import router
# from src.schedule import schedule_parsing


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    """'Обертка' для реализации событий до и после запуска приложения"""
    print('Server starts')
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
