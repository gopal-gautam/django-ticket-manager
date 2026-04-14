#!/bin/bash

# Entrypoint script that runs before the Django server starts
# This script ensures the database is ready and migrations are applied

echo "Waiting for PostgreSQL to be ready..."

# Wait for PostgreSQL to accept connections
# This loops until it can successfully connect to the database
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

# Apply any pending database migrations
python manage.py migrate --noinput

echo "Migrations complete - starting Django server"

# Execute the command passed to docker (usually the Gunicorn command)
exec "$@"
