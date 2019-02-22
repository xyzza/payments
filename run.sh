#!/usr/bin/env bash
sleep 5
echo "Running migration..."
yoyo apply -d $DB_DSN
echo "Migration complete..."

echo ""
echo "Starting server..."
python manage.py runserver