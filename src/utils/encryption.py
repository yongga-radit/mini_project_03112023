import os
import base64
import binascii
import json

from Crypto import Random
from Crypto.Cipher import AES
from pydantic import BaseSettings
from dotenv import load_dotenv

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from fastapi.encoders import jsonable_encoder

load_dotenv()
PASSPHRASE = os.getenv('PASSPHRARSE_SECRET')
PASSCODE = os.getenv('PASSCODE')
TOKEN = APIKeyHeader(name='Authorization')


def encode_data(data: dict):
    global PASSPHRASE
    json_encoder = jsonable_encoder(data)
    data_json_b64 = base64.b64encode(json.dumps(json_encoder).encode('ascii'))
    try:
        key = binascii.unhexlify(PASSPHRASE)
        iv = Random.get_random_bytes(AES.block_size)
        cipher = AES.new(key, AES.MODE_GCM, iv)
        encrypted, tag = cipher.encrypt_and_digest(data_json_b64)
        encrypted_64 = base64.b64encode(encrypted).decode('ascii')
        iv_64 = base64.b64encode(iv).decode('ascii')
        tag_64 = base64.b64encode(tag).decode('ascii')
        json_data = {'iv': iv_64, 'data': encrypted_64, 'tag': tag_64}
        encrypted_data = base64.b64encode(json.dumps(json_data).encode('ascii')).decode('ascii')
        return encrypted_data
    except:
        return ''


def validate_token(token: str = Depends(TOKEN)) -> dict:
    global PASSPHRASE
    if token:
        token = token.split(' ')
        if not token[0] == "Bearer":
            raise HTTPException(status_code=403, detail="Invalid autentication schema.")
        if not decode_data(token=token[1]):
            raise HTTPException(status_code=403, detail="Invalid token.")
        return decode_data(token=token[1])
    else:
        raise HTTPException(status_code=403, detail="Invalid authorization token.")


def decode_data(token: str) -> bool:
    global PASSPHRASE
    is_token_valid: bool = False
    try:
        key = binascii.unhexlify(PASSPHRASE)
        encrypted = json.loads(base64.b64decode(token).decode('ascii'))
        encrypted_data = base64.b64decode(encrypted['data'])
        iv = base64.b64decode(encrypted['iv'])
        tag = base64.b64decode(encrypted['tag'])
        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted = cipher.decrypt_and_verify(encrypted_data, tag)
        result_decrypt = json.loads(base64.b64decode(decrypted).decode('ascii'))
        payload = result_decrypt
    except:
        payload = None

    if payload is not None and "credentials" in payload \
                            and payload['credentials'] == PASSCODE:
        is_token_valid = payload
    else:
        is_token_valid = None
    
    return is_token_valid