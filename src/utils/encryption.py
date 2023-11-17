import os
import base64
import binascii
import json
import jwt
import fastapi as _fa

from Crypto import Random
from Crypto.Cipher import AES
from pydantic import BaseSettings
from dotenv import load_dotenv
from src.database import database as _db

from sqlalchemy.orm import Session

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from fastapi.encoders import jsonable_encoder
from src.utils.get_payload import get_payload
from src.config import config as _config

load_dotenv()
TOKEN = APIKeyHeader(name='Authorization')
# PASSPHRASE = os.getenv('PASSPHRARSE_SECRET')


def validate_token(token: str = Depends(TOKEN)) -> dict:
    try:
        decoded_data = jwt.decode(
            token, _config.config.PRIVATE_KEY, ['HS256']
        )
        return decoded_data
    except jwt.ExpiredSignatureError:
        return {"message": "Token has expired"}
    except jwt.InvalidSignatureError:
        return {"message": "Signature verification failed"}
    except jwt.InvalidTokenError as e:
        return {"message": f"Invalid token. Details: {str(e)}"}
