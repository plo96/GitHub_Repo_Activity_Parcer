"""
   Кастомные exceptions для приложения.
"""
from abc import ABC, abstractmethod

from fastapi import status


class CustomException(Exception, ABC):
    """Родительский класс для всех кастомных исключений."""
    
    @property
    @abstractmethod
    def detail(self):
        ...
    

class CustomHTTPException(CustomException, ABC):
    """Родительский класс для всех кастомных HTTP-исключений."""
    
    @property
    @abstractmethod
    def status_code(self):
        ...


class TooFewRepos(CustomHTTPException):
    """Не удалось выгрузить установленное параметрами количество репозиториев."""
    
    def __init__(self, limit: int = None, current_len: int = None):
        """
        :param limit: Установленное число репозиториев в топе.
        :param current_len: Число репозиториев, полученных в результате запроса.
        """
        self.limit = limit
        self.current_len = current_len
    
    @property
    def detail(self) -> str:
        return f"Database get only {self.current_len} elements, but limit is {self.limit}"
    
    @property
    def status_code(self) -> str:
        return status.HTTP_507_INSUFFICIENT_STORAGE


class NoRepoActivities(CustomHTTPException):
    """В базе нет данных касательно изменений запрашиваемого репозитория за данный период."""
    
    @property
    def detail(self) -> str:
        return "Activities for this period is not found."
    
    @property
    def status_code(self) -> str:
        return status.HTTP_404_NOT_FOUND


class NoRepoOwnerCombination(CustomHTTPException):
    """В базе нет комбинации такого репозитория и владельца."""
    
    @property
    def detail(self) -> str:
        return "Combination for this owner and repo is not found."
    
    @property
    def status_code(self) -> str:
        return status.HTTP_404_NOT_FOUND


class AddNewDataError(CustomException):
    """Ошибка при добавлении новых данных в базу."""
    
    @property
    def detail(self) -> str:
        return "Error: application can not add fresh data to database."


class ParsingNewDataError(CustomException):
    """Ошибка при парсинге новых данных."""
    
    @property
    def detail(self) -> str:
        return "Error: application can not parse GitHub to take a fresh data."
