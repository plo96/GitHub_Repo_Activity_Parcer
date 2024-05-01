# sudo docker build -t git_top_app -f Dockerfile.app .
# sudo docker run --rm -p 8000:8000 git_top_app

FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY alembic.ini alembic.ini

COPY ./migrations/ migrations/

COPY src src

# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
