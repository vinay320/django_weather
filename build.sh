#!/bin/bash

# Build the project

echo "Building the project..."
python3.12 -m pip install -r requirements.txt

echo "Making Migrations..."
python3.12 manage.py makemigrations --noinput
python3.12 manage.py migrate --noinput

echo "Collecting Static Files..."
python3.12 manage.py collectstatic --noinput --clear
