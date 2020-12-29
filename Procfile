web: gunicorn salud_publica.wsgi --log-file -
worker: celery -A salud_publica beat -l info -S django

