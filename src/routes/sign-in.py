import sqlalchemy as _sa
import pydantic as _pd
import fastapi as _fa

from typing import Optional
from sqlalchemy.orm import Session
from src.database import database as _db
from src.models import users as Users
from werkzeug.security import generate_password_hash
from utils.generate_token import generate_refresh_token


class LoginData(_pd.BaseModel):
    email: str
    password: str


async def signin(data: LoginData, db: Session):
    # check email on db
    user = db.query(Users.User.email).filter(Users.User.email == data.email).exists().scalar()

    if user is None:
        raise _fa.HTTPException(400, detail="User not found.")
    else:
        encrypted_password = generate_password_hash(data.password)
        if encrypted_password != user.password:
            _fa.HTTPException(400, detail="Password Incorrect!")
    
    payload = {
        'uid': user.id,
        'email': data.email
    }

    refresh_token = generate_refresh_token(payload)
    
