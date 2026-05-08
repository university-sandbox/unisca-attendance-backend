#!/bin/sh
set -e

uv run python manage.py collectstatic --noinput
uv run python manage.py migrate --noinput

if [ "$#" -eq 1 ]; then
  exec sh -c "$1"
fi

exec "$@"
