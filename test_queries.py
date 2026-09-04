import os
import django
from django.conf import settings

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
        'django_otp.plugins.otp_totp',
        'rest_framework',
        'corsheaders',
        'campaigns',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
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
    TID='dummy',
    TTK='dummy',
    NUMTEL='dummy',
    NUMWHA='dummy',
    TNUMBER='dummy',
    TWILIO_ACCOUNT_SID='dummy',
    TWILIO_AUTH_TOKEN='dummy',
    TWILIO_NUMBER='dummy',
    MAILGUN_API_KEY='dummy',
    MAILGUN_URL='dummy',
    MAILGUN_DOMAIN='dummy',
    T_AUTH_TOKEN='dummy',
)

django.setup()
from django.core.management import call_command
call_command('migrate')

from campaigns.models import Campania, estado_campania, Operador, mediosxcampania, Medio, Tipo_medio
from campaigns.viewsets import CampaignViewSet
from rest_framework.test import APIRequestFactory
import datetime
from django.db import connection

def test_campaign_list_queries():
    est = estado_campania.objects.create(descripcion=1)
    op = Operador.objects.create(email="test@test.com", clave="123")
    tm = Tipo_medio.objects.create(descripcion=1)

    for i in range(20):
        c = Campania.objects.create(
            nombre=f"Camp {i}",
            fechaInicio=datetime.date.today(),
            fechaFin=datetime.date.today() + datetime.timedelta(days=1),
            duracion=1,
            operador_ID=op,
            estado=est
        )
        m = Medio.objects.create(tipo_medio=tm)
        mediosxcampania.objects.create(
            campania_id=c,
            medio_id=m,
            intensidad=1,
            hora1=datetime.time(10, 0)
        )

    factory = APIRequestFactory()
    request = factory.get('/api/campaigns/')
    view = CampaignViewSet.as_view({'get': 'list'})

    initial_queries = len(connection.queries)
    response = view(request)
    queries = len(connection.queries) - initial_queries

    import json
    for q in connection.queries[initial_queries:]:
        if 'campaigns_campania' in q['sql'] and 'LIMIT 21' in q['sql']:
            print("FOUND BAD QUERY: ", q['sql'])
            break

    assert response.status_code == 200
    print(f"Number of queries for list action with 20 items: {queries}")

test_campaign_list_queries()
