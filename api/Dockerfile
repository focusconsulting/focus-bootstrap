FROM python:3.12.3-slim as build

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN pip install 'poetry==1.8.2'
RUN apt-get update \
    && apt-get install --no-install-recommends --yes \
    postgresql libpq-dev gnupg build-essential

# DEV Build
FROM build as dev

EXPOSE 8000

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

RUN poetry config virtualenvs.in-project true \
    && poetry install --no-interaction --no-ansi --no-root

CMD ["poetry", "run", "uvicorn", "focus_api.__main__:app", "--reload", "--host=0.0.0.0"]


# Non-dev build
FROM build as app-build

WORKDIR /app

RUN poetry config virtualenvs.in-project true
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --without dev

# Prod
FROM python:3.12.3-slim as app

RUN apt-get update \
    && apt-get install --no-install-recommends --yes libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 999 python && \
    useradd -r -u 999 -g python python

RUN mkdir /app && chown python:python /app
WORKDIR /app

COPY --chown=python:python --from=app-build /app/.venv /app/.venv
COPY --chown=python:python . .

USER 999

ENV PATH="/app/.venv/bin:$PATH"
CMD [ "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "focus_api.__main__:app" ]