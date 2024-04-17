import pytest
from sqlalchemy.ext.asyncio import AsyncSession


async def test_get_top_100(repos_url: str, async_client: AsyncSession, some_repo_added: None):
	
	result = await async_client.get(url=repos_url + 'top100')
	print(result.json())
