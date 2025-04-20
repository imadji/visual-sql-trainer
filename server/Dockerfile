FROM python:3.12-slim

RUN apt-get update && apt-get install -y postgresql-client

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml /app/

RUN poetry install --no-root

COPY . /app

EXPOSE 8000

CMD ["poetry", "run", "python", "main.py"]