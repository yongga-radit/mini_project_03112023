import sqlalchemy as _sa
import pydantic as _pd
import fastapi as _fa

from sqlalchemy.orm import Session
from src.models import book_stocks as _bs, users as _u
from src.depends import authentication as _auth
from typing_extensions import Optional


async def delete_product(book_id: int, payload: dict, db: Session):
    user_id = payload.get("uid", 0)
    admin = db.query(_u.User).filter(_u.User.id == user_id).first()
    if admin.user_role != 1:


    return {"message": "Successfully deleted."}