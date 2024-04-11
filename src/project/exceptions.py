"""
   Кастомные exceptions для данного приложения;
   Декоратор для обработки исключений;
"""
from functools import wraps

from fastapi import HTTPException, status


def exceptions_processing(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ObjectNotFoundError as _ex:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"{_ex.object_type} with this {_ex.parameter} is not found in database")
        except Exception as _ex:
            print(_ex)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Unknown internal server error")

    return wrapper


class ObjectNotFoundError(Exception):
    """Не удалось найти объект с указанными параметрами в базе"""
    def __init__(self, object_type: str = None, parameter: str = None):
        self.object_type = object_type
        self.parameter = parameter
