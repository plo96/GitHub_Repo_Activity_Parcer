"""
	Основные слои для работы с приложением:
	 - routers для реализации запросов по API;
	 - services для реализации бизнес-логики;
	 - repositories для взаимодействия с базой данных для конкретных сущностей.
"""
__all__ = (
	'repositories',
	'services',
	'routers',
)

from . import repositories, services, routers
