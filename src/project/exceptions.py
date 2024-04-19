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
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{_ex.object_type} with this {_ex.parameter} is not found in database",
            )
        except TooFewRepos as _ex:
            raise HTTPException(
                status_code=status.HTTP_507_INSUFFICIENT_STORAGE,
                detail=f"Database get only {_ex.current_len} elements, but limit is {_ex.limit}",
            )
        except Exception as _ex:
            print(_ex)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unknown internal server error",
            )

    return wrapper


class ObjectNotFoundError(Exception):
    """Не удалось найти объект с указанными параметрами в базе"""
    def __init__(self, object_type: str = None, parameter: str = None):
        self.object_type = object_type
        self.parameter = parameter


class TooFewRepos(Exception):
    """Не удалось выгрузить установленное параметрами количество репозиториев"""
    def __init__(self, limit: int = None, current_len: int = None):
        self.limit = limit
        self.current_len = current_len
