import sqlalchemy as _sa
import pydantic as _pd
import fastapi as _fa

from typing import Optional
from sqlalchemy.orm import Session
from src.database import database as _db
from src.models import users as _u
from werkzeug.security import generate_password_hash
from src.depends import base_response as _response


class RegisterData(_pd.BaseModel):
    name: str
    email: str
    password: str
    confirm_password: str
    role: int
    parent_id: Optional[int]

    @_pd.root_validator
    def check_confirm_password(cls, vals):
        password = vals.get('password')
        confirm_password = vals.get('confirm_password')

        if confirm_password != password:
            raise _fa.HTTPException(422, 'Password does not match!')

        return vals


async def signup(
    data: RegisterData,
):
    db: Session = _fa.Depends(_db.get_db)

    # check if email already existed
    email_exist = db.query(_u.User).filter(
                            _u.User.email == data.email).first()
    if email_exist:
        raise _fa.HTTPException(400, detail="Email have already been used.")

    parent_exist = db.query(_u.User).filter(_u.User.id == data.parent_id).first
    if not parent_exist:
        raise _fa.HTTPException(400, detail="parent_id does not exist.")

    encrypted_password = generate_password_hash(data.password)

    # add data to db 
    user = _u.User(
        email=data.email,
        name=data.name,
        password=encrypted_password,
        user_role=data.role,
        parent_id=data.parent_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return _response.BaseResponseModel(message='user has been created.')
