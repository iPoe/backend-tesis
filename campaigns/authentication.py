import jwt
from rest_framework.authentication import BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from django.conf import settings
from django.contrib.auth import get_user_model

class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        #Return a reason instead of a http response
        return reason
        