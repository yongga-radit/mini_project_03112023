import sqlalchemy as _sa
from src.database import database as _db
import sqlalchemy.orm as _orm
import datetime as _dt


class Books(_db.Base):
    __tablename__ = 'inventory'
    # for save the available books 

    id = _sa.Column('id', _sa.Integer, primary_key=True, index=True)
    title = _sa.Column('title', _sa.String, index=True)
    tag = _sa.Column('tag', _sa.VARCHAR(3))
    barcode = _sa.Column('barcode', _sa.String)
    author = _sa.Column('author', _sa.String)
    publisher = _sa.Column('publisher', _sa.String)
    edition = _sa.Column('published_date', _sa.Integer)
    availability = _sa.Column('quantity', _sa.Integer)
    created_at = _sa.Column('created_at', _sa.DateTime, default=_sa.func.now())
    last_modified = _sa.Column('last_modified', _sa.DateTime, default=_sa.func.NOW(), onupdate=_sa.func.NOW())


class Loan(_db.Base):
    __tablename__ = 'loan'
    # for note users who book the stock

    id = _sa.Column('id', _sa.Integer, primary_key=True, index=True)
    book_id = _sa.Column('book_id', _sa.Integer, _sa.ForeignKey("inventory.id"))
    booking_reference = _sa.Column('reference', _sa.String)
    user_name = _sa.Column('name', _sa.String)
    loan_date = _sa.Column('loan_date', _sa.Date, default=_sa.func.now())
    duration = _sa.Column('duration', _sa.Integer, default=7)
    return_date = _sa.Column('return_date', _sa.Date)
    fine = _sa.Column('fine', _sa.FLOAT, default=0)
    amount = _sa.Column('amount', _sa.Integer, default=1)

    book = _orm.relationship("Book", back_populates="loans")
