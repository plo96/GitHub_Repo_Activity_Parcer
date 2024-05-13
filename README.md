# GitHub Repo Activity Parcer
## Описание

GitHub Repo Activity Parcer - простое веб-приложение на python с API для получения информации о топе репозиториев в GitHub по звёздам и активностях (число и авторы коммитов за один день) конкретного 
репозитория по дням. Также включает в себя периодический асинхронный парсер GitHub по RestAPI для обновления данных.

### Реализованы технологии:
- RestAPI на базе FastAPI;
- Обращение с данными через Pydantic-схемы;
- Реляционная база данных на основе PostgreSQL;
- Асинхронный доступ к БД;
- Миграции БД;
- Асинхронное выполнение задач по расписанию;;
- Основная структура приложения разделена на слои:
    - Роутеры - для взаимодействия с пользователем
    - Сервисы - для осуществления бизнес-логики
    - Репозитории - для взаимодействия с БД
- Дополнительно:
  - Код покрыт тестами;
  - Собраны и настроены docker-compose файлы для запуска приложения и тестов (по отдельности).

## Основной используемый стек технологий:

- Python:
  - FastAPI
  - SQLAlchemy
  - psycopg3
  - Alembic
  - APScheduler
  - httpx
  - pytest
- PostgreSQL
- docker, docker-compose

## Запуск и настройка

Для запуска данного приложения необходимо проделать следующие шаги:
1) Скопировать к себе удалённый репозиторий данного приложения.
2) Установить на машину утилиты Docker и Docker-compose.
3) Зарегистрироваться на GitHub.com и получить личный токен для доступа к API сайта:
   >github.com --> profile --> Settings --> Developer Settings --> Personal access token --> Fine-grained token
4) Создать в директории с приложением файл .env и внести туда следующие данные (подставить в поле API_KEY полученный в предыдущем шаге токен и не забыть заменить пароль в поле DB_PASSWORD)::
    ```plaintext
        APP_HOST_PORT=8000                   # Порт на рабочей машине, по которому будет доступно API приложения.  

        DB_PORT=5432                         # Порт на рабочей машине, по которому будет достунеп контейнер с PostgreSQL.
        DB_HOST=postgres                     # Хост для подключения к БД из приложения (имя контейнера).
        DB_NAME=postgres                     # Имя базы данных.
        TEST_DB_NAME=test_postgres           # Имя тестовой базы данных.
        DB_USER=postgres                     # Имя пользователя базы данных.
        DB_PASSWORD=YOUR_PASSWORD            # Пароль пользователя базы данных.

        ECHO=FALSE                           # Отображение логов обращения к БД (True/FalseS).
        TEST_ECHO=FALSE                      # Отображение логов обращения к БД (True/FalseS).

        API_KEY=PASTE_YOUR_API_KEY_HERE      # Полученный в п.3 индивидуальный токен GitHub.

5) Находясь в директории с приложением выполнить в терминале команду:
  - 'docker-compose up --build -d '- для запуска контейнеров с БД и приложением.
  - 'docker-compose -f docker-compose-tests.yml up --build -d' - для запуска контейнеров с БД и тестами.
  - 'docker logs -f my_app' - для интерактивного вывода логов приложения или тестов в консоль системы.
  - 'docker-compose down' --remove-orphans - остановка всех работающих контейнеров и их удаление.
___
  **Во время работы приложения доступны endpoits для API:** 
* /api/repos/top100 - *получение списка топа репозиториев GitHub по звёздам.*
* /api/repos/{owner}/{repo}/activity - *получение для конкретного репозитория списка активностей по дням за запрошенный период.*

## Примечания:
1) Более подробную информацию по деталям запроса и ответов можно найти в swagger данного приложения (http://"host":"port"/docs)
2) Запросы в виде сырого SQL и f-строки - не баг, а фича (захотелось немного вспомнить SQL). 
П.С. SQL-инъекции не проходят, т.к. execute пропускает только одну команду.
3) При запуске приложения всегда происходит первоначальный асинхронный парсинг GitHub. В случае первого запуска придётся подождать пока соберутся необходимые данные.
4) Число отслеживаемых репозиториев можно изменить параметром **LIMIT_TOP_REPOS_LIST** в файле **app.src.core.models.repos**.
5) Время задержки между двумя последовательными запросами к API GitHub можно изменить параметром **DEFAULT_PAUSE_VALUE** в файле **app.src.schedule.schedule_parser**.