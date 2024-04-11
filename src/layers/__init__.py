"""
	Основные слои для работы с приложением:
	 - routers для реализации запросов;
	 - services для реализации бизнес-логики;
	 - repositories для взаимодействия с базой данных.
"""
__all__ = (
	'repositories',
	'services',
	'routers',
)

from . import repositories, services, routers
