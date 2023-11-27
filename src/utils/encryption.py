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

from fastapi import Depends
from fastapi.security import APIKeyHeader
from fastapi.encoders import jsonable_encoder
from src.utils.get_payload import get_payload
from src.config import config as _config

load_dotenv()
TOKEN = APIKeyHeader(name='Authorization')
# PASSPHRASE = os.getenv('PASSPHRARSE_SECRET')


def validate_token(token: str = Depends(TOKEN)) -> dict:
    try:
        token.split('')
        if token[0] != 'Basic':
            _fa.HTTPException(400, detail="Token Invalid")
        
        decoded_data = jwt.decode(
            token[1], _config.config.PRIVATE_KEY, ['HS256']
        )
        return decoded_data
    except jwt.ExpiredSignatureError:
        raise _fa.HTTPException(400, detail="Token has expired")
    except jwt.InvalidSignatureError:
        raise _fa.HTTPException(400, detail="Signature verification failed")
    except jwt.InvalidTokenError as e:
        raise _fa.HTTPException(400, detail=f"Invalid token. Details: {str(e)}")
