import sqlalchemy as _sa
import pydantic as _pd
import fastapi as _fa

from typing import Optional
from sqlalchemy.orm import Session
from src.database import database as _db
from src.models import users as Users
from werkzeug.security import generate_password_hash

class ForgotData(_pd.BaseModel):
    # when change password on login interface
    credential: str
    password: str
    confirm_password: str

    @_pd.root_validator
    def validate_p