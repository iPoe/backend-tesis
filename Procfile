web: gunicorn salud_publica.wsgi --log-file -
worker: celery -A salud_publica worker --loglevel=info
worker: celery -A salud_publica beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler