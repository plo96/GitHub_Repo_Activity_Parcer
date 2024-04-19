import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.repos import DEFAULT_SORT_PARAM, LIMIT_TOP_REPOS_LIST


@pytest.mark.parametrize(
	"param",
	[
		None,
		"stars",
		"repo",
		"owner",
		"position_cur",
		"position_prev",
		"watches",
		"forks",
		"open_issues",
		"language",
		"_smth_",
	]
)
async def test_get_top(param: str | None, repos_url: str, async_client: AsyncSession, some_repos_added: None):
	param_url_suffix = f'?param={param}'
	if not param:
		param_url_suffix = ""
		param = DEFAULT_SORT_PARAM
		
	result = await async_client.get(repos_url + 'top100' + param_url_suffix)
	assert result.status_code == 200
	assert len(result.json()) == LIMIT_TOP_REPOS_LIST
	
	if param == "_smth_":
		param = DEFAULT_SORT_PARAM
	list_of_params = [i[param] for i in list(result.json())]
	sorted_list = list_of_params.copy()
	sorted_list.sort(reverse=True)
	assert list_of_params == sorted_list
	

@pytest.mark.parametrize(
	"param",
	[
		None,
		"stars",
		"repo",
		"owner",
		"position_cur",
		"position_prev",
		"watches",
		"forks",
		"open_issues",
		"language",
		"_smth_",
	]
)
async def test_get_top_with_few_data(param: str, repos_url: str, async_client: AsyncSession, a_few_repos_added: None):
	param_url_suffix = ""
	if param:
		param_url_suffix = f'?param={param}'
	result = await async_client.get(repos_url + 'top100' + param_url_suffix)
	assert result.status_code == 507
