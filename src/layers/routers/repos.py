"""
	Роутер для описания возможностей внешнего взаимодействия с репозиториями
"""
from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_session
from src.project.exceptions import exceptions_processing
from src.core.schemas import RepoDTO, RepoActivityDTO
from src.layers.services import RepoService

router = APIRouter(tags=['Repos'], prefix="/repos")


@router.get("/top100")
@exceptions_processing
async def get_top_100(
		session: AsyncSession = Depends(get_session),
) -> list[RepoDTO]:
	return await RepoService.get_top_100_repos(session=session)


@router.get("/{owner}/{repo}/activity")
@exceptions_processing
async def get_activity(
		owner: str,
		repo: str,
		since: date,
		until: date,
		session: AsyncSession = Depends(get_session),
) -> list[RepoActivityDTO]:
	return await RepoService.get_activity(
		session=session,
		owner=owner,
		repo=repo,
		since=since,
		until=until,
	)
