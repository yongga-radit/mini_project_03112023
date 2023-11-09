import pydantic as _pd
import fastapi as _fa
import sqlalchemy as _sa

from sqlalchemy.orm import Session
from src.database import database as _db
from src.models import users as Users


class LogoutData(_pd.BaseModel):
    # refresh_token: str
    user_id: int


async def signout(
    data: LogoutData, 
    db: Session
):
    # check the user's refresh token 
    result = db.query(Users.UserLogin).filter(
                Users.UserLogin.user_id == data.user_id).all()

    # if token not found
    if not result:
        raise _fa.HTTPException(400, 'Refresh token not found')

    db.delete(result)  
    db.commit()
    return _fa.Response(status_code=204)
