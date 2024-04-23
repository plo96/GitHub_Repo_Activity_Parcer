from uuid import UUID, uuid4


def get_str_uuid() -> str:
	"""Функция для получения значения uuid по умолчанию"""
	uuid: UUID = uuid4()
	return uuid.__str__()
