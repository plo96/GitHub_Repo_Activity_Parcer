"""
	Роутер для описания возможностей внешнего взаимодействия с репозиториями
"""
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_session
from src.project.decorators import router_exceptions_processing
from src.core.schemas import RepoUpload
from src.layers.services import RepoService

router = APIRouter(tags=['Repos'], prefix="/repos")


@router.get("/top100")
@router_exceptions_processing
async def get_top(
		param: Optional[str] = None,
		session: AsyncSession = Depends(get_session),
) -> list[RepoUpload]:
	"""
	Возвращение топа репозиториев с сортировкой по заданному параметру модели.
	:param param: Параметр для сортировки. По умолчанию - количество звёзд.
	:param session: Сессия для доступа к БД. Получение из зависимостей.
	:return: Список моделей репозитория для выгрузки.
	"""
	return await RepoService.get_top_repos(
		session=session,
		param=param,
	)
