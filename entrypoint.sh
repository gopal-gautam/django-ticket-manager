#!/bin/bash

set -e

echo "Waiting for PostgreSQL to be ready..."

until python -c "import psycopg2; psycopg2.connect(
    host='${POSTGRES_HOST}',
    port='${POSTGRES_PORT}',
    dbname='${POSTGRES_DB}',
    user='${POSTGRES_USER}',
    password='${POSTGRES_PASSWORD}'
)"; do
    echo "PostgreSQL is unavailable - sleeping"
    sleep 2
done

echo "PostgreSQL is available - running migrations"

python manage.py migrate --noinput

echo "Migrations complete - collecting static files"

python manage.py collectstatic --noinput --clear

echo "Static files collected - starting Django server"

exec "$@"
