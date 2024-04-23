"""
	Роутер для описания возможностей внешнего взаимодействия с репозиториями
"""
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_session
from src.project.decorators import router_exceptions_processing
from src.core.schemas import RepoUpload, RepoActivityUpload
from src.layers.services import RepoService, RepoActivitiesService

router = APIRouter(tags=['Repos'], prefix="/repos")


@router.get("/top100")
@router_exceptions_processing
async def get_top(
		param: Optional[str] = None,
		session: AsyncSession = Depends(get_session),
) -> list[RepoUpload]:
	return await RepoService.get_top_repos(session=session, param=param)


@router.get("/{owner}/{repo}/activity")
@router_exceptions_processing
async def get_activity(
		owner: str,
		repo: str,
		since: date,
		until: date,
		session: AsyncSession = Depends(get_session),
) -> list[RepoActivityUpload]:
	return await RepoActivitiesService.get_activity(
		session=session,
		owner=owner,
		repo=repo,
		since=since,
		until=until,
	)
