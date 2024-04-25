"""
	Роутер для описания возможностей внешнего взаимодействия с активностями репозаториев
"""
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_session
from src.project.decorators import router_exceptions_processing
from src.core.schemas import RepoActivityUpload
from src.layers.services import RepoActivitiesService

router = APIRouter(tags=['Repos'], prefix="/repos")


@router.get("/{owner}/{repo}/activity")
@router_exceptions_processing
async def get_activity(
		owner: str,
		repo: str,
		since: Optional[date] = None,
		until: Optional[date] = None,
		session: AsyncSession = Depends(get_session),
) -> list[RepoActivityUpload]:
	"""
	Вовзращение информации об активностях конкретного репозитория за некоторый промежуток времени.
	:param owner: Владелец репозитория на GitHub.
	:param repo: full_name репозитория на GitHub.
	:param since: Начальная точка по времени для выборки.
	:param until: Конечная точка по времени для выборки.
	:param session: Сессия для доступа к БД. Получение из зависимостей.
	:return: Список ативности в репозиториях по дням за указанный период.
	"""
	return await RepoActivitiesService.get_activity(
		session=session,
		owner=owner,
		repo=repo,
		since=since,
		until=until,
	)
