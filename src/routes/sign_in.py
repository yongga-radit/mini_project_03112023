import sqlalchemy as _sa
import pydantic as _pd
import fastapi as _fa

from sqlalchemy.orm import Session
from src.models import users as Users
from src.config import config as _config
from werkzeug.security import check_password_hash
from src.utils.generate_token import generate_refresh_token, generate_access_token
from src.depends import base_response as _response


class LoginData(_pd.BaseModel):
    # for login interface
    email: str
    password: str

class DataResponse(_pd.BaseModel):
    # for returning login data with token
    user_id: int
    email: str
    person: str
    role: int
    refresh_token: str
    access_token: str
    expired_at: int

class LoginResponseModel(_response.BaseResponseModel):
    # returning status if login success
    data: DataResponse


async def signin(data: LoginData, db: Session):
    # check email on db
    user = db.query(Users.User).filter(
                    Users.User.email == data.email).first()
    
    # if user and password doesn't match
    if user is None:
        raise _fa.HTTPException(400, detail="User not found.")
    else:
        # encrypted_password = generate_password_hash(data.password)
        # if encrypted_password != user.password:
        if not check_password_hash(user.password, data.password):
            raise _fa.HTTPException(400, detail="Password Incorrect!")
    
    # get data to generate token
    payload = {
        'uid': user.id,
        'email': data.email   
    }

    # check if the user already login before by checking the token
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
    db.refresh()

    access_token, access_token_expired_at = generate_access_token(payload)

    # inject token to user login response model
    return LoginResponseModel(
        data=DataResponse(
            user_id=user.id,
            person=user.name,
            email=user.email,
            role=user.role,
            access_token=access_token,
            refresh_token=refresh_token,
            expired_at=access_token_expired_at

        )
    )
