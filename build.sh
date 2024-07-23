#!/bin/bash

# Build the project

echo "Building the project..."
python -m pip install -r requirements.txt

echo "Making Migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Collecting Static Files..."
python manage.py collectstatic --noinput --clear
