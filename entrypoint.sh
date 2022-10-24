#! /bin/bash
python manage.py runserver 0.0.0.0:8000
gunicorn --bind 0.0.0.0:8000 similarity_text.wsgi --reload

