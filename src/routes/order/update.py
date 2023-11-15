import sqlalchemy as _sa
import pydantic as _pd
import fastapi as _fa

from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from src.models import book_stocks as _bs, users as _u
from src.depends import base_response as _response, authentication as _auth
from typing_extensions import Optional, List


async def return_book(
    loan_id: int,
    db: Session,
    payload: dict,
    fine_per_day: float = 5000.0
):
    user_id = payload.get('uid', False)
    # if user_id.user_role != 1:  # if not admin
    #     _fa.HTTPException('Input data only by Admin')
    
    loan = db.query(_bs.Loan).filter(
                                _bs.Loan.id == loan_id and _bs.Loan.user_id == user_id).first()

    if not loan:
        raise _fa.HTTPException('Data not found')
    
    end_date = loan.loan_date + timedelta(days=loan.duration)
    loan.return_date = datetime.now().date()

    if loan.return_date > end_date:
        days = loan.return_date - end_date
        loan.fine = days * fine_per_day

    book = db.query(_bs.Books).filter(_bs.Books.id == loan.book_id).first()
    book.availability += loan.amount
    loan.status = "returned"
    
    db.commit()

    return _response.BaseResponseModel(
            data={   
                    "order_id": loan.id,
                    "start_date": loan.loan_date,
                    "expired_date": loan.loan_date + timedelta(
                                                    days=loan.duration),
                    "return_date": loan.return_date,
                    "fine": loan.fine
                },
            )
