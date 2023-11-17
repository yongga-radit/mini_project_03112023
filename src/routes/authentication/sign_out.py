import pydantic as _pd
import fastapi as _fa
import sqlalchemy as _sa

from sqlalchemy.orm import Session
from src.database import database as _db
from src.models import users as Users


async def signout(
    # payload: dict,
    access_token: str,
    db: Session
):
    # user_id = payload.get("uid", False)
    
    # check the user's refresh token 
    result = db.query(Users.UserLogin).filter(
                Users.UserLogin.access_token == access_token).first()
    # result = db.query(Users.UserLogin).filter(
    #             Users.UserLogin.user_id == int(user_id).all()

    # if token not found
    if result is None:
        raise _fa.HTTPException(400, 'Refresh token not found')
    db.delete(result)  
    db.commit()
    return _fa.Response(status_code=204)
