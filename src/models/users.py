import sqlalchemy as _sa
from datetime import date, datetime
from src.database import database as _db
import sqlalchemy.orm as _orm


class User(_db.Base):
    __tablename__ = 'user'
    # for save user data

    id = _sa.Column('id', _sa.Integer, primary_key=True)
    name = _sa.Column('name', _sa.VARCHAR(256))
    email = _sa.Column('email', _sa.VARCHAR(255))
    # 1.Admin, 2.Head,  3. Employee
    user_role = _sa.Column('user_role', _sa.Integer)
    password = _sa.Column('password', _sa.String)
    created_at = _sa.Column('created_at', _sa.DateTime, default=datetime.today())
    modified_at = _sa.Column('modified_at', _sa.DateTime,
                            default=datetime.today(), onupdate=datetime.today())
    last_activity = _sa.Column('last_activity', _sa.DateTime,
                            default=datetime.today(), onupdate=datetime.today())
    # user_info = _sa.Column("user_info", back_populates="parent")


class UserInfo(_db.Base):
    __tablename__ = 'user_info'

    id = _sa.Column('id', _sa.Integer, primary_key=True)
    user_id = _sa.Column(_sa.Integer, _sa.ForeignKey("users.id"))
    full_name = _sa.Column('full_name', _sa.VARCHAR(255))
    created_at = _sa.Column('created_at', _sa.DateTime,
                            default=datetime.today())
    updated_at = _sa.Column('updated_at', _sa.DateTime,
                            default=datetime.today(), onupdate=datetime.today())
    # parent = _orm.relationship("user", back_populates="children")

class UserLogin(_db.Base):
    __tablename__ = 'user_login'
    # for save user who login using token

    id = _sa.Column('id', _sa.Integer, primary_key=True)
    user_id = _sa.Column('user_id', _sa.Integer)
    refresh_token = _sa.Column('refresh_token', _sa.String)
    access_token = _sa.Column('access_token', _sa.String)
    expired_at = _sa.Column('expired_at', _sa.DateTime)
    created_at = _sa.Column('created_at', _sa.DateTime, default=datetime.today())
    modified_at = _sa.Column('modified_at', _sa.DateTime,
                            default=datetime.today(), onupdate=datetime.today())
