FROM python:3.12-slim

RUN apt-get update && apt-get install -y postgresql-client curl

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

RUN poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml /app/
RUN poetry install --no-interaction --no-root

COPY . /app

EXPOSE 8000

CMD ["poetry", "run", "python", "main.py"]
