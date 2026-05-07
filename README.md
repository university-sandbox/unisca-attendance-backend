# UNISCA Attendance Backend

Django REST API for the UNISCA attendance system.

## Requirements

- Python 3.12+
- uv
- Docker and Docker Compose, if running with containers

## Environment

Create a local `.env` file from the example:

```bash
cp .env.example .env
```

Update at least `SECRET_KEY` and `DB_PASSWORD` before running locally.

## Install

```bash
uv sync
```

## Run Locally

Start PostgreSQL separately, then run:

```bash
uv run python manage.py migrate
uv run python manage.py runserver 0.0.0.0:8000
```

The API will be available at:

```text
http://localhost:8000
```

## Run With Docker Compose

```bash
docker compose up --build
```

This starts:

- PostgreSQL on the internal Docker network
- Django on `http://localhost:8000`

## Notes

The current bootstrap config points `AUTH_USER_MODEL` to `usuarios.Usuario`. That model is introduced in the next implementation phase, so `migrate`, `manage.py check`, and the backend Docker build will work after the Phase 2 models are added.
