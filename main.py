from typing import List
import fastapi as _fa
import fastapi.security as _security
import sqlalchemy.orm as _orm
from src.database import database as _db
from src.models import users as User
import src.routes as _endpoint

api = _fa.APIRouter()

_db.create_database()

# api.add_api_route('/user/sign-up', signup,
#                          methods=['POST'], tags=['User'], status_code=200)

