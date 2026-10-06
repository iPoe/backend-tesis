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
        'django_celery_beat',
        'django_otp',
        'django_otp.plugins.otp_totp',
        'rest_framework',
        'corsheaders',
        'campaigns',
    ],
    SECRET_KEY='dummy',
    TID='dummy',
    T_AUTH_TOKEN='dummy',
    TNUMBER='dummy',
    TWAPP='dummy',
    AUTH_USER_MODEL='campaigns.Usuario',
    ROOT_URLCONF='salud_publica.urls',
    MIDDLEWARE=[
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ],
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ],
)

django.setup()
call_command('migrate')

from django.test.utils import get_runner
TestRunner = get_runner(settings)
test_runner = TestRunner(verbosity=2, interactive=True)
failures = test_runner.run_tests(['campaigns.tests'])
import sys
sys.exit(bool(failures))
