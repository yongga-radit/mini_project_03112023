from datetime import datetime as _dt, timedelta as _delta
import jwt
from typing import Tuple

SECRET_KEY = "mini_project_03112023"
REFRESH_TOKEN_EXPIRATION = _delta(days=30)


def generate_refresh_token(payload: dict):
    # after login, user got token to access the website
    expiration = _dt.utcnow() + REFRESH_TOKEN_EXPIRATION
    payload.update({
        'iat': expiration,
        **payload
    })

    refresh_token = jwt.encode(payload, SECRET_KEY, algorithm=['HS256'])

    return refresh_token


def verify_refreshed_token(refresh_token: str):
    # checking the token is correct or not
    try:
        token_data = jwt.decode(refresh_token, 
                                SECRET_KEY, 
                                algorithms=['HS256'])
        return token_data
    except jwt.ExpiredSignatureError:
        # handle token expiration
        return None
    except jwt.DecodeError:
        # handle token decoding error
        return None