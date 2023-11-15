import sqlalchemy as _sa
import pydantic as _pd
import fastapi as _fa

from datetime import datetime, date
from typing import Optional
from sqlalchemy.orm import Session
from src.database import database as _db
from src.models import users as Users
from src.depends import authentication as _auth
from src.utils.encryption import validate_token
from werkzeug.security import generate_password_hash


class UpdatePassword(_pd.BaseModel):
    new_password: str
    confirm_new_password: str

    @_pd.root_validator
    def validate_new_password(cls, vals: dict):
        password = vals.get('new_password')
        confirm_password = vals.get('confrim_new_password')

        if password != confirm_password:
            raise _fa.HTTPException(422, 'New Password does not match.')


async def update_password(
    # when change password on account settings
    data: UpdatePassword,
    db: Session,
    payload: dict = _fa.Depends(validate_token)
):
    user_id = payload.get('uid', False)

    if not user_id:
        raise _fa.HTTPException('You must login first.')

    encrypted_password = generate_password_hash(data.new_password)

    user = db.query(Users.User).filter(Users.User.id == user_id).first()
    user.password = encrypted_password

    db.commit()

    return _fa.Response(status_code=201)


class UpdateUserInfo(_pd.BaseModel):
    # Users
    username: str
    # User Info
    first_name: str
    last_name: str
    phone: str
    occupation: Optional[str]
    institution: Optional[str]
    birthday: date


async def update_info(
    data: UpdateUserInfo,
    payload: _fa.Depends(_auth.Authentication()),
    db: Session
):
    user_id = payload.get('uid', 0)

    user = db.query(Users.User).filter(
                Users.User.id == user_id).first()

    user_info = db.query(Users.UserInfo).filter(Users.UserInfo.id == user.id)

    add_info = Users.UserInfo(
                    user_id=user_id,
                    first_name=data.first_name,
                    last_name=data.last_name,
                    phone=data.phone,
                    occupation=data.occupation,
                    institution=data.institution,
                    birthday=data.birthday
                )
    if not user_info:
        add_info = Users.UserInfo(update_at=datetime.today())

    db.add(add_info)
    db.commit()

    return _fa.Response(status_code=200)
