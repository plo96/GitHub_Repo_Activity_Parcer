"""
    Кастомные декораторы
"""
from functools import wraps
from asyncio import sleep as asleep

from fastapi import HTTPException

from .exceptions import CustomHTTPException, status, ParsingNewDataError


def router_exceptions_processing(func):
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
                detail="Unknown internal server error",
            )

    return wrapper


def multiply_parsing_trying(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        for _ in range(5):
            result = await func(*args, **kwargs)
            if result:
                break
            await asleep(5)
        else:
            raise ParsingNewDataError
        return result
    
    return wrapper
