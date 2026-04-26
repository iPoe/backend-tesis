import os
import django
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salud_publica.settings')
os.environ['SECRET_KEY'] = 'test'
os.environ['postdbName'] = 'test'
os.environ['post_user'] = 'test'
os.environ['post_password'] = 'test'
os.environ['postHost'] = 'test'
os.environ['postPort'] = '5432'
django.setup()

from campaigns.models import *
from campaigns.tasks import llamar_usuarias
from django.test import TestCase

# Not easy to mock all of this.
# Instead let's write a unit test style measurement if possible.
