import sqlalchemy as _sa
import pydantic as _pd
import fastapi as _fa

from typing import Optional
from sqlalchemy.orm import Session
from src.database import database as _db
from src.models import users as Users
from src.config import config as _config
from werkzeug.security import generate_password_hash
from utils.generate_token import generate_refresh_token, generate_access_token


class LoginData(_pd.BaseModel):
    email: str
    password: str


async def signin(data: LoginData, db: Session):
    # check email on db
    user = db.query(Users.User.email).filter(
                    Users.User.email == data.email).exists().scalar()

    # if user and password doesn't match
    if user is None:
        raise _fa.HTTPException(400, detail="User not found.")
    else:
        encrypted_password = generate_password_hash(data.password)
        if encrypted_password != user.password:
            _fa.HTTPException(400, detail="Password Incorrect!")
    
    # get data to generate token
    payload = {
        'uid': user.id,
        'email': data.email,      
    }

    refresh_token = generate_refresh_token(payload)
    user_signin = Users.UserLogin(
        user_id=user.id,
        refresh_token=refresh_token,
        expired_at=_sa.func.TIMESTAMPADD(
            _sa.text('SECOND'),
            _config.config.REFRESH_TOKEN_EXPIRATION,
            _sa.func.NOW()
        )
    )

    # save the token on user
    db.add(user_signin)
    db.commit()

    access_token, access_token_expired_at = generate_access_token(payload)

    
