import os
import django
from django.conf import settings
from django.core.management import call_command
import sys

settings.configure(
    DEBUG=True,
    SECRET_KEY='dummy',
    INSTALLED_APPS=[
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django_celery_beat',
        'django_otp',
        'rest_framework',
        'corsheaders',
        'campaigns',
    ],
    AUTH_USER_MODEL='campaigns.Usuario',
    ROOT_URLCONF='salud_publica.urls',
    MIDDLEWARE=[
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware'
    ],
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ]
        }
    }],
    TID='dummy', TTK='dummy', NUMTEL='dummy', NUMWHA='dummy', T_AUTH_TOKEN='dummy', TNUMBER='dummy',
    MAILGUN_API_KEY='dummy', MAILGUN_URL='dummy', MAILGUN_DOMAIN='dummy',
    TWILIO_ACCOUNT_SID='dummy', TWILIO_AUTH_TOKEN='dummy', TWILIO_NUMBER='dummy',
    EMAIL_USER='dummy', EMAIL_PASSWORD='dummy'
)
django.setup()

import unittest
test_suite = unittest.TestLoader().discover('campaigns')
unittest.TextTestRunner(verbosity=2).run(test_suite)
