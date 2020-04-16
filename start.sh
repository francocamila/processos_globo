#!/bin/bash

#while ! pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -q -U $POSTGRES_USER; do
#  >&2 echo "Postgres is unavailable - sleeping...";
#  sleep 5;
#done;
#>&2 echo "Postgres is up - executing commands...";
sleep 15;
echo '======= RUNNING PIP INSTALL'
pip install --no-cache-dir -r requirements.txt

#echo '======= MAKING MIGRATIONS'
#python3 manage.py makemigrations

#echo '======= RUNNING MIGRATIONS'
#python3 manage.py migrate

#echo '======= COLLECTING STATIC'
#python manage.py collectstatic --noinput

#gunicorn qrcode.wsgi -b 0.0.0.0:8000

echo '======= RUNNING SERVER'
python3 manage.py runserver 0.0.0.0:8000