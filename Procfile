web : gunicorn salud_publica.wsgi
worker : celery -A salud_publica worker --beat --scheduler django --loglevel=info
