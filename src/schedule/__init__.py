"""
	Модуль для задач, выполняемых по расписанию.
"""
__all__ = (
	"init_scheduler",
)

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .schedule_parsing import schedule_parser


async def init_scheduler() -> None:
	"""
	Инициализация объекта класса AsyncIOScheduler и	добавление в него всех задач по расписанию.
	Предварительный вызов нужных процессов во время первоначального запуска расписания.
	:return: None
	"""
	async_scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
	await schedule_parser.task_processing()
	async_scheduler.add_job(schedule_parser.task_processing, trigger="interval", days=1)
	async_scheduler.start()
