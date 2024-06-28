#!/bin/sh

# Start Redis server
service redis-server start

# Wait for the server volume to be available
until cd /app/project-video/
do
    echo "Waiting for server volume..."
done

# Wait for the database to be ready
until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

# Collect static files
python manage.py collectstatic --noinput

# Start Celery worker
celery -A projectx worker --loglevel=info &

# Start Celery beat
celery -A projectx beat --loglevel=info &

# Start Django server
python manage.py runserver 0.0.0.0:8000
