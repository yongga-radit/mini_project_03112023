import sqlalchemy as _sa
from src.database import database as _db


class User(_db.Base):
    __tablename__ = 'User'
    # for save user data

    id = _sa.Column('id', _sa.Integer, primary_key=True)
    name = _sa.Column('name', _sa.VARCHAR(256))
    email = _sa.Column('email', _sa.VARCHAR(255))
    # 1.Admin, 2.Moderator, 3.Instructor, 4. Learners
    user_role = _sa.Column('user_role', _sa.Integer)
    password = _sa.Column('password', _sa.VARCHAR(255))
    created_at = _sa.Column('created_at', _sa.DateTime, default=_sa.func.NOW())
    modified_at = _sa.Column('modified_at', _sa.DateTime,
                            default=_sa.func.NOW(), onupdate=_sa.func.NOW())


class UserLogin(_db.Base):
    __tablename__ = 'UserLogin'
    # for save user who login using token

    id = _sa.Column('id', _sa.Integer, primary_key=True)
    user_id = _sa.Column('user_id', _sa.Integer)
    refresh_token = _sa.Column('refresh_token', _sa.String)
    expired_at = _sa.Column('expired_at', _sa.DateTime, default=_sa.func.NOW())
    created_at = _sa.Column('created_at', _sa.DateTime, default=_sa.func.NOW())
    modified_at = _sa.Column('modified_at', _sa.DateTime,
                            default=_sa.func.NOW(), onupdate=_sa.func.NOW())


class UserCredForgot(_db.Base):
    __tablename__ = 'UserCredForgot'
    # for save credential user who forgot password

    id = _sa.Column('id', _sa.Integer, primary_key=True)
    user_id = _sa.Column('user_id', _sa.Integer)
    credentials = _sa.Column('credentials', _sa.String)
    used = _sa.Column('used', _sa.DateTime, default=_sa.func.NOW())
    created_at = _sa.Column('created_at', _sa.DateTime, default=_sa.func.NOW())
    updated_at = _sa.Column('updated_at', _sa.DateTime,
                           default=_sa.func.NOW(), onupdate=_sa.func.NOW())
