from functools import lru_cache
from pydantic import BaseSettings


class _Config(BaseSettings):
    APP: str

    ACCESS_TOKEN_EXPIRATION: int 
    REFRESH_TOKEN_EXPIRATION: int 
    PRIVATE_KEY: str 
    PUBLIC_KEY: str 
    REFRESH_PRIVATE_KEY: str 

    class Config:
        env_file = '.env'


@lru_cache
def get_config():
    return _Config()


config = get_config()
