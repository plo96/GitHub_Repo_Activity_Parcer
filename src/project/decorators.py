"""
    Кастомные декораторы для приложения.
"""
from functools import wraps
from asyncio import sleep as asleep

from fastapi import HTTPException

from src.project.exceptions import CustomHTTPException, status, ParsingNewDataError
from src.project.config import settings


def router_exceptions_processing(func):
    """Обработка исключений для роутеров."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except CustomHTTPException as _ex:
            raise HTTPException(
                status_code=_ex.status_code,
                detail=_ex.detail,
            )
        except Exception as _ex:
            print(_ex)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unknown internal server error.",
            )

    return wrapper


def multiply_parsing_trying(max_trying: int):
    """
    Автоматическое повторение попытки парсинга в случае неудачи при парсинге или записи в БД.
    :param max_trying: Максимальное число попыток.
    """
    def outer_wrapper(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for _ in range(max_trying):
                result = await func(*args, **kwargs)
                if result:
                    break
                await asleep(5)
            else:
                raise ParsingNewDataError
            return result

        return wrapper

    return outer_wrapper
