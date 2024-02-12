#!/bin/bash
python manage.py makemigrations
python manage.py migrate
sleep 3
python manage.py makemigrations authentication
python manage.py migrate
python manage.py makemigrations audiofiles
python manage.py makemigrations quiz
python manage.py makemigrations post
python manage.py migrate
python manage.py loaddata data-backup/audiofiles.json
python manage.py loaddata data-backup/post.json
python manage.py loaddata data-backup/quiz.json
