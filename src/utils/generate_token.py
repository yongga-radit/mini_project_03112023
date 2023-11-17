import time
import json
import jwt
from src.config import config as _config
from typing import Tuple
from datetime import timedelta, datetime


def generate_refresh_token(payload: dict) -> str:
    current_time = datetime.today()

    payload.update({
        'iat': current_time.isoformat()
    })

    refresh_token = jwt.encode(
        payload, _config.config.REFRESH_PRIVATE_KEY.encode('utf-8'), 'HS256')

    return refresh_token


def generate_access_token(payload):
    current_time = int(time.time())
    expired_at = current_time + _config.config.ACCESS_TOKEN_EXPIRATION

    payload.update({
        'exp': expired_at,
        'iat': current_time
        # 'exp': expired_at.isoformat(),
        # 'iat': current_time.isoformat()
    })
    
    access_token = jwt.encode(
        payload, _config.config.PRIVATE_KEY.encode('utf-8'), "HS256")

    return access_token, expired_at
