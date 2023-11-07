import time

import jwt
from src.config import config as _config
from typing import Tuple


def generate_refresh_token(payload: str) -> str:
    current_time = int(time.time())

    payload.update({
        'iat': current_time
    })

    refresh_token = jwt.encode(
        payload, _config.config.REFRESH_PRIVATE_KEY.encode('utf-8'), 'HS256')

    return refresh_token


def generate_access_token(payload: str) -> Tuple[str, int]:
    current_time = int(time.time())
    expired_at = current_time + _config.config.ACCESS_TOKEN_EXPIRATION

    payload.update({
        'exp': expired_at,
        'iat': current_time
    })

    access_token = jwt.encode(
        payload, _config.config.PRIVATE_KEY.encode('utf-8'), "HS256")

    return access_token, expired_at
