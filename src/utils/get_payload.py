import jwt

from src.config import config as _config


def get_payload(access_token: str, verify_exp: bool = True) -> dict:
    # return random string into payload/ data
    payload = jwt.decode(access_token, _config.config.PRIVATE_KEY, [
                         'HS256'], option={'verify_exp': verify_exp})

    return payload
