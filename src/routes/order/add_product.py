import sqlalchemy as _sa
import pydantic as _pd
import fastapi as _fa

from sqlalchemy.orm import Session
from src.models import book_stocks as _bs, users as _u
from src.depends import authentication as _auth
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
    payload: dict = _fa.Depends(_auth.Authentication())
):
    user_id = payload.get('uid', False)

    admin = db.query(_u.User).filter(_u.User.id == user_id).first()

    if admin.user_role != 0:
        _fa.HTTPException(400, detail='Input data only by Admin')

    existed_book = db.query(_bs.Books).filter(
                            _bs.Books.barcode == data.barcode).first()
    if existed_book:
        existed_book.title = data.book_name,
        existed_book.tag = data.tag,
        existed_book.author = data.author,
        existed_book.publisher = data.publisher,
        existed_book.edition = data.edition,
        existed_book.availability = data.availability

        db.commit()
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
