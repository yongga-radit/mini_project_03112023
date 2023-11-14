import sqlalchemy as _sa
import pydantic as _pd
import fastapi as _fa

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.models import book_stocks as _bs, users as _u
from src.depends import base_response as _response, authentication as _auth
from typing_extensions import Optional


class RegisterProduct(_pd.BaseModel):
    book_name: str
    publisher: str
    barcode: str
    edition: Optional[int]
    tag: Optional[str]
    author: Optional[str]
    availability: int


# to create/ edit book data
async def register_book(
    data: RegisterProduct,
    db: Session,
    payload = _fa.Depends(_auth.Authentication())
):
    
    user_id = payload.get('uid', 0)
    if user_id.user_role != 1:  # if not admin
        _fa.HTTPException('Input data only by Admin')

    existed_book = db.query(_bs.Books).filter(
                            _bs.Books.barcode == data.barcode).first()
    if existed_book:
        existed_book(
            title=data.book_name,
            tag=data.tag,
            author=data.author,
            publisher=data.publisher,
            edition=data.edition,
            availability=data.availability
        )
    else:
        new_book = _bs.Books(
            title=data.book_name,
            tag=data.tag,
            barcode=data.barcode,
            author=data.author,
            publisher=data.publisher,
            edition=data.edition,
            availability=data.availability
        )

        db.add(new_book)
        db.commit()
        db.refresh(new_book)

    return _fa.Response(status_code=201)


class OrderInput(_pd.BaseModel):
    customer_id: int
    customer_name: Optional[str]
    book_id: int
    # barcode: Optional[str]
    # id_number: Optional[str]
    # start_date: datetime.date = _sa.func.now()
    duration: int
    amount: float


async def order(
    data: OrderInput,
    db: Session,
    payload= _fa.Depends(_auth.Authentication())
):
    user_id = payload.get('uid', 0)
    # if user_id.user_role != 1:  # if not admin
    #     _fa.HTTPException('Input data only by Admin')

    customer = db.query(_u.User).filter(_u.User.id == data.customer_id).first()
    book = db.query(_bs.Books).filter(
                                    _bs.Books.id == data.book_id).first()
    if book is None:
        _fa.HTTPException('Book not found')

    leftover = book.availability - data.amount
    if leftover < 0:
        _fa.HTTPException(404, detail="Stock Insufficient. Please check the book's availibity.")
    book.availability = leftover

    # reference = book.tag + data.start_date.year \
    #                         + '/' + data.start_date.month \
    #                         + '/' + data.start_date.day + '/'

    add_order = _bs.Loan(
                    book_id=data.book_id,
                    # booking_reference=reference,
                    user_name=customer.name if customer else data.customer_name,
                    duration=data.duration,
                    amount=data.amount
                )
    db.add(add_order)
    db.commit()
    db.refresh(add_order)

    return _response.BaseResponseModel(
            data={   
                    "customer_name": customer.name if customer else data.customer_name,
                    "order_id": add_order.id,
                    "start_date": datetime.now(),
                    "expired_date": add_order.loan_date + timedelta(
                                                        days=data.duration),
                    "created_by_id": user_id
                },
            )


class ReturnBook(_pd.BaseModel):
    reference: Optional[str]
    book_id: Optional[int]
    loan_id: int
    fine_per_day: Optional[float]


async def return_book(
    data: ReturnBook,
    db: Session,
    payload = _fa.Depends(_auth.Authentication)
):
    user_id = payload.get('uid', 0)
    if user_id.user_role != 1:  # if not admin
        _fa.HTTPException('Input data only by Admin')
    
    book_loaned = db.query(_bs.Loan).filter(
                                _bs.Loan.id == data.loan_id).first()
    
    if not book_loaned:
        raise _fa.HTTPException('Data not found')
    
    end_date = book_loaned.loan_date + timedelta(days=book_loaned.duration)
    book_loaned.return_date = _sa.func.now()

    if book_loaned.return_date > end_date:
        days = book_loaned.return_date - end_date
        book_loaned.fine = days * data.fine_per_day
    
    return _response.BaseResponseModel(
            data={   
                    "created_by_id": user_id,
                    "order_id": book_loaned.id,
                    "start_date": book_loaned.loan_date,
                    "expired_date": book_loaned.loan_date + timedelta(
                                                    days=book_loaned.duration),
                    "return_date": book_loaned.return_date,
                    "fine": book_loaned.fine
                },
            )
