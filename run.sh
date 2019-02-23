#!/usr/bin/env bash
./wait-for-postgres.sh $DB_HOST:$DB_PORT

echo "Running migration..."
yoyo apply -d $DB_DSN
echo "Migration complete..."

echo "Running test..."
pytest

echo ""
echo "Starting server..."
python manage.py runserver