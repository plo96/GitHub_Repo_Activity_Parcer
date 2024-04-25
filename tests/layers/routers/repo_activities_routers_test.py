from datetime import date
from random import choice

from httpx import AsyncClient

from src.project.exceptions import NoRepoActivities, NoRepoOwnerCombination


async def test_get_repo_activities(
		some_repo_activities_added: None,
		repos_url: str,
		owners_repos_with_activities: list[tuple],
		since_until: tuple[date, date],
		async_client: AsyncClient,
):
	owner, repo = choice(owners_repos_with_activities)
	since, until = since_until
	result = await async_client.get(repos_url + f'{owner}/{repo}/activity?since={since}&until={until}')
	assert result.status_code == 200
	for ans in result.json():
		assert isinstance(ans, dict)
		assert list(ans.keys()) == ['date', 'commits', 'authors']


async def test_get_repo_activities_without_since(
		some_repo_activities_added: None,
		repos_url: str,
		owners_repos_with_activities: list[tuple],
		since_until: tuple[date, date],
		async_client: AsyncClient,
):
	owner, repo = choice(owners_repos_with_activities)
	_, until = since_until
	result = await async_client.get(repos_url + f'{owner}/{repo}/activity?until={until}')
	assert result.status_code == 200
	for ans in result.json():
		assert isinstance(ans, dict)
		assert list(ans.keys()) == ['date', 'commits', 'authors']


async def test_get_repo_activities_without_until(
		some_repo_activities_added: None,
		repos_url: str,
		owners_repos_with_activities: list[tuple],
		since_until: tuple[date, date],
		async_client: AsyncClient,
):
	owner, repo = choice(owners_repos_with_activities)
	since, _ = since_until
	result = await async_client.get(repos_url + f'{owner}/{repo}/activity?since={since}')
	assert result.status_code == 200
	for ans in result.json():
		assert isinstance(ans, dict)
		assert list(ans.keys()) == ['date', 'commits', 'authors']


async def test_get_repo_activities_bad_dates(
		some_repo_activities_added: None,
		repos_url: str,
		owners_repos_with_activities: list[tuple],
		since_until: tuple[date, date],
		async_client: AsyncClient,
):
	owner, repo = choice(owners_repos_with_activities)
	since, until = since_until
	since = until.replace(year=until.year + 1)
	until = until.replace(year=until.year + 2)
	result = await async_client.get(repos_url + f'{owner}/{repo}/activity?since={since}&until={until}')
	assert result.status_code == 404
	assert result.json()['detail'] == NoRepoActivities().detail


async def test_get_repo_activities_bad_fullname(
		some_repo_activities_added: None,
		repos_url: str,
		owners_repos_with_activities: list[tuple],
		since_until: tuple[date, date],
		async_client: AsyncClient,
):
	owner, repo = choice(owners_repos_with_activities)
	since, until = since_until
	result = await async_client.get(repos_url + f'{owner}/{repo[:-1]}/activity?since={since}&until={until}')
	assert result.status_code == 404
	assert result.json()['detail'] == NoRepoOwnerCombination().detail


async def test_get_repo_activities_bad_owner(
		some_repo_activities_added: None,
		repos_url: str,
		owners_repos_with_activities: list[tuple],
		since_until: tuple[date, date],
		async_client: AsyncClient,
):
	owner, repo = choice(owners_repos_with_activities)
	since, until = since_until
	result = await async_client.get(repos_url + f'{owner[:-1]}/{repo}/activity?since={since}&until={until}')
	assert result.status_code == 404
	assert result.json()['detail'] == NoRepoOwnerCombination().detail
