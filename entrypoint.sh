#!/bin/bash
python ./unitysphere/manage.py makemigrations --noinput
python ./unitysphere/manage.py migrate --noinput
python ./unitysphere/manage.py loaddata ./unitysphere/fixtures/auth.json
python ./unitysphere/manage.py loaddata ./unitysphere/fixtures/content.json
cd ./unitysphere
gunicorn core.wsgi:application --bind 0.0.0.0:8000
