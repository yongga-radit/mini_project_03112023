from functools import lru_cache
from pydantic import BaseSettings
from typing_extensions import Optional


class _Config(BaseSettings):
    APP: Optional[str]

    ACCESS_TOKEN_EXPIRATION: int = 24 * 60 * 60
    REFRESH_TOKEN_EXPIRATION: int = 30 * 24 * 60 * 60
    PRIVATE_KEY: str 
    PUBLIC_KEY: str 
    REFRESH_PRIVATE_KEY: str 

    class Config:
        env_file = '.env'


@lru_cache
def get_config():
    return _Config()


config = get_config()
