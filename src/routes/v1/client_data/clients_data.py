import sqlalchemy as _sa
import pydantic as _pd
import fastapi as _fa

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.models import users as _u, clients as _c
from src.config import config as _config
from src.utils.encryption import validate_token
from src.database import database as _db
from src.depends import base_response as _response


class ClientData(_pd.BaseModel):
    name: str
    email: str
    client_type_id: int
    client_industries_id: int
    pic_client: str
    pic_contact: str


async def InputClientData(
    data: ClientData,
    payload: dict = _fa.Depends(validate_token)
):
    db: Session = _fa.Depends(_db.get_db)

    uid = payload.get('uid', 0)
    admin = db.query(_u.User).filter(_u.User.id == uid).first()
    if admin.user_role != 1:
        _fa.HTTPException(400, detail='Input only by Admin')

    check_name = db.query(_c.Client).filter(_c.Client.name == data.name).first()
    if check_name:
        _fa.HTTPException(400, detail=f'Client already exists. id:{check_name.id}')

    client = _c.Client(
        name=data.name,
        email=data.email,
        client_type_id=data.client_type_id,
        client_industries_id=data.client_industries_id,
        pic_client=data.pic_client,
        pic_contact=data.pic_contact,
        user_id=uid
    )

    db.add(client)
    db.commit()
    db.refresh(client)

    return _response.BaseResponseModel(message='client has been created.')
