import sqlalchemy as _sa
import pydantic as _pd
import fastapi as _fa

from typing import Optional
from sqlalchemy.orm import Session
from src.database import database as _db
from src.models import users as Users
from werkzeug.security import generate_password_hash


class RegisterData(_pd.BaseModel):
    name: str
    email: str
    password: str
    confirm_password: str
    role: int

    @_pd.root_validator
    def check_confirm_password(cls, vals):
        password = vals.get('password')
        confirm_password = vals.get('confirm_password')

        if confirm_password != password:
            raise _fa.HTTPException(422, 'Password does not match!')
        
        return vals
    
    
async def signup(
        data: RegisterData, 
        # db: Session = _fa.Depends(_db.get_db)
        db: Session
        ):
    # check if email already existed
    email_exist = db.query(Users.User).filter(
                            Users.User.email == data.email).first()

    # email_exist = db.execute(
    #     _sa.select(
    #         User.User.id
    #     ).where(
    #         User.User.email == data.email
    #     )
    # ).fetchone()

    if email_exist:
        raise _fa.HTTPException(400, detail="Email have already been used.")
    
    encrypted_password = generate_password_hash(data.password)

    # add data to db 
    user = Users.User(
        email=data.email,
        name=data.name,
        password=encrypted_password,
        user_role=data.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return _fa.Response(status_code=201)
