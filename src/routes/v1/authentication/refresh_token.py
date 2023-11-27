import sqlalchemy as _sa
import pydantic as _pd
import fastapi as _fa

from typing import Optional
from sqlalchemy.orm import Session
from src.database import database as _db
from src.models import users as Users
from src.depends import base_response as _response, authentication as _auth
from src.utils.generate_token import generate_access_token
from src.config.config import config
from datetime import timedelta, datetime

class AccessToken(_pd.BaseModel):
    access_token: str


# save the output 
class RefreshTokenResponseData(_pd.BaseModel):
    access_token: str
    expired_at: int


class RefreshTokenResponse(_response.BaseResponseModel):
    data: RefreshTokenResponseData

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'refresh_token': '123.456.789',
                    'expired_at': 123456
                },
                'meta': {},
                'message': 'Success',
                'success': True,
                'code': 200
            }
        }


async def refresh_token(
    data: AccessToken, 
    db: Session, 
    payload = _fa.Depends(_auth.Authentication())
):
    
    # check refresh token
    user_login = db.query(Users.UserLogin).filter(
                    Users.UserLogin.user_id == Users.User.id,
                    Users.UserLogin.refresh_token == data.refresh_token
                    ).first()
    
    if not user_login:
        raise _fa.HTTPException(400, detail='Refresh token not found.')

    # if user_login.expired_at > _dt.datetime.now():
    if user_login.expired_at > _sa.func.now():
        raise _fa.HTTPException(403, detail={
                'message': 'Refresh token is expired.',
                'code': 40301
            }
        )
    
    expired_in_seconds = config.REFRESH_TOKEN_EXPIRATION
    current_time = _sa.func.now()
    user_login.expired_at = current_time + timedelta(
                                seconds=expired_in_seconds)
    
    user = db.query(Users.User).filter(
                    Users.User.id == user_login.user_id
                    ).first()
    # generate new access token
    payload = {
        'uid': user_login.user_id,
        'email': user.email
    }

    access_token, expired_at = generate_access_token(payload)
    db.commit()

    return RefreshTokenResponse(
        data=RefreshTokenResponseData(
            access_token=access_token,
            expired_at=expired_at
        )
    )
