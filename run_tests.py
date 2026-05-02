import os
import django
from django.conf import settings
from django.core.management import call_command

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=[
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'django_celery_beat',
        'campaigns',
    ],
    AUTH_USER_MODEL='campaigns.Usuario',
    SECRET_KEY='secret',
    ROOT_URLCONF='salud_publica.urls',  # Fixed URLConf to point to the main project
    MIDDLEWARE=[
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ],
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ],
    TID='test_sid',
    T_AUTH_TOKEN='test_token',
    TNUMBER='test_number',
    WNUMBER='test_whatsapp',
    EMAIL_HOST_USER='test_email',
    EMAIL_HOST_PASSWORD='test_password',
)

django.setup()

call_command('test', 'campaigns')
