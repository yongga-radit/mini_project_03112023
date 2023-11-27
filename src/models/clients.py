import sqlalchemy as _sa
import sqlalchemy.orm as _orm

from datetime import date, datetime
from src.database import database as _db


class Client(_db.Base):
    __tablename__ = 'clients'

    id = _sa.Column('id', _sa.Integer, primary_key=True)
    name = _sa.Column('name', _sa.VARCHAR(256))
    email = _sa.Column('email', _sa.VARCHAR(255))
    client_type_id = _sa.Column('client_type_id', _sa.Integer)
    client_industries_id = _sa.Column('client_industries_id', _sa.Integer)
    pic_client = _sa.Column('pic_client', _sa.VARCHAR(255))
    pic_contact = _sa.Column('pic_contact', _sa.String)
    created_at = _sa.Column('created_at', _sa.DateTime, default=datetime.today())
    modified_at = _sa.Column('modified_at', _sa.DateTime,
                            default=datetime.today(), onupdate=datetime.today())

    user_id = _sa.Column('user_id', _sa.Integer, _sa.ForeignKey("users.id"))


class ClientType(_db.Base):
    __tablename__ = 'client_types'

    id = _sa.Column('id', _sa.Integer, primary_key=True)
    type = _sa.Column('type', _sa.VARCHAR(256))


class ClientIndustry(_db.Base):
    __tablename__ = 'client_industries'

    id = _sa.Column('id', _sa.Integer, primary_key=True)
    industries = _sa.Column('industries', _sa.VARCHAR)


class ClientBudget(_db.Base):
    __tablename__ = 'client_budget'

    id = _sa.Column('id', _sa.Integer, primary_key=True)
    client_id = _sa.Column('client_id', _sa.Integer, _sa.ForeignKey('clients.id'))
    budget = _sa.Column('budget', _sa.Float)
    period_start = _sa.Column('loan_date', _sa.Date)
    commit_month = _sa.Column('duration', _sa.Integer)
    period_end = _sa.Column('return_date', _sa.Date)
    # 1: HOLD; 2: RUNNING; 3: DONE
    status = _sa.Column('status', _sa.Integer)
    created_at = _sa.Column('created_at', _sa.DateTime, default=datetime.today())
    modified_at = _sa.Column('modified_at', _sa.DateTime,
                            default=datetime.today(), onupdate=datetime.today())