from uuid import UUID, uuid4


def get_uuid() -> UUID:
	"""Функция для получения значения uuid по умолчанию"""
	return uuid4()
