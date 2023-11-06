import pydantic as _pd
import fastapi as _fa
import sqlalchemy.orm as Session

from src.database import database as _db
from src.models import users as Users


class LogoutData(_pd.BaseModel):
    refresh_token: str


async def signout(data: LogoutData, db: Session = _fa.Depends(_db.get_db)):
    result = db.query(Users.UserLogin).filter(
                Users.UserLogin.refresh_token == data.refresh_token).delete()
    
    # if token not found
    if not result:
        raise _fa.HTTPException(400, 'Refresh token not found')
    
    db.commit()

    return _fa.Response(status_code=204)
