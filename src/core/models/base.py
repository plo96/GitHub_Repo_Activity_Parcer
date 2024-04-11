"""
    Инициализация базового класса для последующего наследования от него всех ОРМ-моделей
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
	"""Базовый класс для всех ОРМ-моделей для аккумуляции metadata"""
	pass
