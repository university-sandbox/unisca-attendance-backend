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
uv run python manage.py seed
uv run python manage.py runserver 0.0.0.0:8000
```

The API will be available at:

```text
http://localhost:8000
```

## Seed Data

Load Spanish demo data with:

```bash
uv run python manage.py seed
```

To recreate only the demo data managed by the seed:

```bash
uv run python manage.py seed --reset
```

Default demo password:

```text
Demo12345!
```

## Run With Docker Compose

```bash
docker compose up --build
```

This starts:

- PostgreSQL on the internal Docker network
- Django on `http://localhost:8000`

The backend container automatically runs pending migrations before starting Django.

## Dokploy deployment

The Docker image runs Nginx in front of Gunicorn. Nginx serves user uploads at
`/media/` and forwards API requests to Django.

Add a Dokploy **Volume Mount** before the first production upload:

- Volume name: `unisca-media`
- Mount path: `/app/media`

The volume is required because the Docker image intentionally excludes `media/`.
Without it, uploaded profile photos are lost when Dokploy replaces the container
during a deployment.

## Notes

The current bootstrap config points `AUTH_USER_MODEL` to `usuarios.Usuario`. That model is introduced in the next implementation phase, so `migrate`, `manage.py check`, and the backend Docker build will work after the Phase 2 models are added.
