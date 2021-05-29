web: gunicorn salud_publica.wsgi --log-file -
worker: celery -A salud_publica worker --loglevel=info
worker2: celery -A salud_publica beat -l info -S django