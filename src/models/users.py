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
    # 1.Admin, 2.User
    user_role = _sa.Column('user_role', _sa.Integer)
    password = _sa.Column('password', _sa.String)
    created_at = _sa.Column('created_at', _sa.DateTime, default=datetime.today())
    modified_at = _sa.Column('modified_at', _sa.DateTime,
                            default=datetime.today(), onupdate=datetime.today())
    # user_info = _sa.Column("user_info", back_populates="parent")


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


class UserCredForgot(_db.Base):
    __tablename__ = 'user_cred_forgot'
    # for save credential user who forgot password

    id = _sa.Column('id', _sa.Integer, primary_key=True)
    user_id = _sa.Column('user_id', _sa.Integer)
    credentials = _sa.Column('credentials', _sa.String)
    used = _sa.Column('used', _sa.DateTime, default=datetime.today())
    created_at = _sa.Column('created_at', _sa.DateTime, default=datetime.today())
    modified_at = _sa.Column('updated_at', _sa.DateTime,
                           default=datetime.today(), onupdate=datetime.today())
    

class UserInfo(_db.Base):
    __tablename__ = 'user_info'

    id = _sa.Column('id', _sa.Integer, primary_key=True)
    # user_id = _sa.Column(_sa.Integer, _sa.ForeignKey("users.id"))
    user_id = _sa.Column('user_id', _sa.Integer)
    first_name = _sa.Column('first_name', _sa.VARCHAR(255))
    last_name = _sa.Column('last_name', _sa.VARCHAR(255))
    phone = _sa.Column('phone', _sa.CHAR(20))
    occupation = _sa.Column('occupation', _sa.VARCHAR(256))
    updated_at = _sa.Column('updated_at', _sa.DateTime,
                           default=datetime.today(), onupdate=datetime.today())
    # parent = _orm.relationship("user", back_populates="children")
    

