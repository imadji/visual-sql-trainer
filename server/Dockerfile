FROM python:3.12-slim

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml /app/

RUN poetry install --no-root

COPY . /app

EXPOSE 8080

CMD ["poetry", "run", "python", "main.py"]