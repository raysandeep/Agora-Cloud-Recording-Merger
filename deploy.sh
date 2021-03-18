#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    while ! nc -z "$DATABASE_URL"; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

#python manage.py flush --no-input
python manage.py migrate
python manage.py collectstatic
nohup celery -A backend worker -l info &
exec "$@"