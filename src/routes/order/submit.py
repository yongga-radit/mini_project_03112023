import sqlalchemy as _sa
import pydantic as _pd
import fastapi as _fa

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.models import book_stocks as _bs, users as _u
from src.depends import base_response as _response, authentication as _auth
from typing_extensions import Optional, List


async def check_status(loan_id: int, payload: dict, db: Session):  # by borrower
    user_id = payload.get("uid", False)
    loan = db.query(_bs.Loan).filter(_bs.Loan.id == loan_id and _bs.Loan.user_id == user_id).first()
    return {
                "user_id": user_id,
                "loan_id": loan.id,
                "status": loan.status
            }


async def post(loan_id: int, is_confirmed: bool, payload: dict, db: Session):  # by admin
    user_id = payload.get("uid", False)
    admin = db.query(_u.User).filter(_u.User.id == user_id).first()
    if admin.user_role != 1:
        _fa.HTTPException(400, detail="Input must by Admin")
    
    loan = db.query(_bs.Loan).filter(_bs.Loan.id == loan_id).first()

    if not loan_id:
        _fa.HTTPException(400, detail="Loan not found")
    
    if is_confirmed: 
        loan.status = "confirmed"
    else:
        loan.status = "rejected"
    loan.loan_date = datetime.now()
    return {
                "user_id": user_id,
                "loan_id": loan_id,
                "status": loan.status,
                "loan_date": loan.loan_date,
                "expired_date": loan.loan_date + timedelta(days=loan.duration)
            }