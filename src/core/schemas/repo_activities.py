from datetime import date as date_type
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class RepoActivityBase(BaseModel):
	"""Базовый класс для активности репозиториев GH"""
	pass


class RepoActivityDTO(RepoActivityBase):
	"""DTO-класс для активности репозиториев GH"""
	repo_id: Optional[str]  				# Уникальное id репозитория (UUID в строке)
	date: date_type  						# Конкретная дата
	commits: int  							# Количество коммитов за конкретный день
	authors: list[str]  					# Список авторов, которые выполняли коммиты

	@staticmethod
	def init_from_parsing_data(
			list_of_commits: list[dict],
	) -> list:
		"""
		Преобразование результата парсинга к модели ДТО
		
		:param repo_id: уникальный идентификатор репозитория
		:param list_of_commits: список всех коммитов (словарей, содержащих автора и дату каждого коммита)
		:return: список объектов данной ДТО-модели
		"""
		
		activities_list: list = []
		
		seen_dates: list = []
		for commit_dict in list_of_commits:
			name, date = commit_dict.get("name"), commit_dict.get("date")
			if date not in seen_dates:
				seen_dates.append(date)
				activity = dict(
					date=date,
					authors={name},
					commits=1,
				)
				activities_list.append(activity)
			else:
				for activity in activities_list:
					if activity.get("date") == date:
						activity["commits"] += 1
						activity["authors"].add(name)
						break
		for index, activity in enumerate(activities_list):
			activity["authors"] = list(activity["authors"])
			activity["repo_id"] = None
			activities_list[index] = RepoActivityDTO.model_validate(**activity)
		
		return activities_list
	
	
class RepoActivityUpload(RepoActivityBase):
	"""Кдасс для передачи по АПИ активности репозиториев GH"""
	date: date_type  						# Конкретная дата
	commits: int  							# Количество коммитов за конкретный день
	authors: list[str]  					# Список авторов, которые выполняли коммиты
