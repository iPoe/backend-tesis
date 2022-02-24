import datetime
import jwt
from django.conf import settings

def generate_access_token(user):
    acces_token_payload = {
        'user_id' : user.id,
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(days = 0, minutes = 5),
        'iat' : datetime.datetime.utcnow(),
    }
    acces_token = jwt.encode(acces_token_payload,
                    settings.SECRE_KEY, algorithm = 'HS256').decode('utf-8')
    return acces_token

def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id' : user.id,
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(days = 7),
        'iat' : datetime.datetime.utcnow(),
    }
    refresh_token = jwt.encode(refresh_token_payload,
                    settings.SECRE_KEY, algorithm = 'HS256').decode('utf-8')
    return refresh_token