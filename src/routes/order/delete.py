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
        _fa.HTTPException(400, detail="Input only by Admin")

    book = db.query(_bs.Books).filter(_bs.Books.id == book_id).first()

    if not book:
        raise _fa.HTTPException(400, detail="Book not found")

    book.is_delete = True
    book.availability = 0

    return {
                "data": book,
                "message": "Successfully deleted."
           }


async def delete_loan(loan_id: int, payload: dict, db: Session):
    user_id = payload.get("uid", 0)
    admin = db.query(_u.User).filter(_u.User.id == user_id).first()
    if admin.user_role != 1:
        _fa.HTTPException(400, detail="Input only by Admin")

    loan = db.query(_bs.Loan).filter(_bs.Loan.id == loan_id).first()

    if not loan:
        raise _fa.HTTPException(400, detail="Loan data not found")

    data = loan
    db.delete(loan)
    db.commit()

    return {
                "data": data,
                "message": "Successfully deleted."
           }
