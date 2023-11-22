import sqlalchemy as _sa
import pydantic as _pd
import fastapi as _fa

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.models import book_stocks as _bs, users as _u
from src.depends import base_response as _response, authentication as _auth
from typing_extensions import Optional, List


async def order(
    book_id: int,
    db: Session,
    payload: dict,
    amount: int = 1
):  # by user
    user_id = payload.get('uid', False)
    customer = db.query(_u.User).filter(_u.User.id == user_id).first()
    
    existed_book = db.query(_bs.Books).filter(
                                    (_bs.Books.id == book_id)
                                    ).first()

    if existed_book is None:
        raise _fa.HTTPException(400, detail="Sorry book is not found")
    leftover = existed_book.availability - amount
    if leftover <= -1:
        raise _fa.HTTPException(400, detail="Book has been borrowed")
    existed_book.availability -= amount

    db.commit()
    # not_found = []
    # no_avail = []
    # for book_id in data.book_ids:
    #     existed_book = db.query(_bs.Books).filter(
    #                                 _bs.Books.id == book_id).first()
    #     if not existed_book:
    #         not_found.append(existed_book.id)
    #     if existed_book.availability == 0:
    #         no_avail.append(existed_book.id)
    #     else:
    #         existed_book.availability -= amount
  
    # if len(not_found) > 0:
    #     not_found_str = ", ".join(map(str, not_found))
    #     _fa.HTTPException(f"Sorry, Book with id: {not_found_str} not found")
    # if len(no_avail) > 0:
    #     no_avail_str = ", ".join(map(str, no_avail))
    #     _fa.HTTPException(f"Book with id: {no_avail_str} have been borrowed")
        
    add_order = _bs.Loan(
                    book_id=book_id,
                    user_id=user_id,
                    user_name=customer.name,
                    duration=7,
                    amount=amount,
                    status="pending"
                )
    
    db.add(add_order)
    db.commit()
    db.refresh(add_order)
    
    return _response.BaseResponseModel(
            data={   
                    "customer_name": customer.name,
                    "order_id": add_order.id,
                    "status": add_order.status
                },
            )


