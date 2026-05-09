FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

ENV POETRY_VIRTUALENVS_CREATE=false

RUN poetry install --no-interaction --no-root

COPY . .

RUN poetry install --no-interaction

EXPOSE 443

CMD [ "poetry", "run", "python3", "src/main.py"]