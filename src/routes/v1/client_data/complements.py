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


async def InputClientTypeData(
    type: str, 
    payload: dict = _fa.Depends(validate_token)
):
    db: Session = _fa.Depends(_db.get_db)

    uid = payload.get('uid', 0)
    admin = db.query(_u.User).filter(_u.User.id == uid).first()
    if admin.user_role != 1:
        _fa.HTTPException(400, detail='Input only by Admin')

    check_name = db.query(_c.ClientType).filter(_c.ClientType.type == type).first()
    if check_name:
        _fa.HTTPException(400, detail=f'Data already exists. id:{check_name.id}')

    client_type = _c.ClientType(type=type)

    db.add(client_type)
    db.commit()
    db.refresh(client_type)

    return _response.BaseResponseModel(message='client type has been created.')


async def InputClientIndustry(
    industry: str,
    payload: dict = _fa.Depends(validate_token) 
):
    db: Session = _fa.Depends(_db.get_db)

    uid = payload.get('uid', 0)
    admin = db.query(_u.User).filter(_u.User.id == uid).first()
    if admin.user_role != 1:
        _fa.HTTPException(400, detail='Input only by Admin')

    check_name = db.query(_c.ClientIndustry).filter(_c.ClientIndustry.industries == industry).first()
    if check_name:
        _fa.HTTPException(400, detail=f'Data already exists. id:{check_name.id}')

    client_industry = _c.ClientType(industries=industry)

    db.add(client_industry)
    db.commit()
    db.refresh(client_industry)

    return _response.BaseResponseModel(message='client industry has been created.')
