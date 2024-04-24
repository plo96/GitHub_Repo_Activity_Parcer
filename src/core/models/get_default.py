"""
	Функции для генерации значений по умолчанию.
"""
from uuid import UUID, uuid4


def get_str_uuid() -> str:
	"""Функция для получения значения uuid (в строковом виде) по умолчанию"""
	uuid: UUID = uuid4()
	return uuid.__str__()
