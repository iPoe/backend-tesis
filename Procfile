web: gunicorn salud_publica.wsgi --log-file -
worker: celery -A salud_publica worker --beat --scheduler django --loglevel=info