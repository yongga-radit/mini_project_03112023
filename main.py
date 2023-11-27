import datetime
import fastapi as _fa
import uvicorn
import jwt
from sqlalchemy.orm import Session, load_only
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from src.database import database as _db
# from src.routes import router
from src.routes.authentication import sign_up, sign_in, sign_out, update_data
from src.routes.order import order, add_product, submit, update, delete
from src.models import users as User, book_stocks
from src.depends import authentication as _auth, authorization as _author
from src.config import config as _config
from src.utils.encryption import validate_token


# creating database
_db.create_database()

# run the program
router = _fa.APIRouter()

router.add_api_route('/user/sign-up', sign_up.signup,
                     methods=['POST'], tags=['Users'])
router.add_api_route('/user/sign-in', sign_in.signin,
                         methods=['POST'], tags=['Users'])
# router.add_api_route('/user/sign-out', sign_out.signout,
#                          methods=['POST'], tags=['Users'])

if __name__ == '__main__':
    uvicorn.run(
        'app:app',
        host="127.0.0.1",
        port=8000,
        reload=True
    )

app = _fa.FastAPI(
  title='Mini Project 03/11/2023',
)

app.include_router(router)

# @app.post("/user/sign-up", tags=["Users"])
# async def registration(
#    data: sign_up.RegisterData,
#    db: Session = _fa.Depends(_db.get_db)
# ):
#     return await sign_up.signup(data=data, db=db)


# @app.post("/user/sign-in", tags=["Users"])
# async def login(
#     data: sign_in.LoginData,
#     db: Session = _fa.Depends(_db.get_db)
# ):
#     return await sign_in.signin(data=data, db=db)


# @app.post("/user/sign-out", tags=["Users"])
# async def logout(
#     # access_token: str,
#     db: Session = _fa.Depends(_db.get_db),
#     payload: dict = _fa.Depends(validate_token)
# ):
#     return await sign_out.signout(payload=payload, db=db)


# @app.post("/user/info", tags=["Users"])
# async def update_user(
#    data: update_data.UpdateUserInfo, 
#    payload: dict = _fa.Depends(validate_token),
#    db: Session = _fa.Depends(_db.get_db)
# ):
#     return await update_data.update_info(data=data, payload=payload, db=db)

# @app.post("/user/reset/password", tags=["User"])
# async def reset_password(
#     data: update_data.UpdatePassword,
#     payload: dict = _fa.Depends(validate_token),
#     db: Session = _fa.Depends(_db.get_db)
# ):
#     return await update_data.update_password(data=data, payload=payload, db=db)


# # ------------------ VALIDATE TOKEN -----------------------------
# @app.get("/token/validate", tags=["token"])
# async def validate_access_token(
#     payload: dict = _fa.Depends(validate_token),
#     db: Session = _fa.Depends(_db.get_db)
# ) -> dict:
#     uid = payload.get('uid', '')
#     email = payload.get('email', '')
#     user = db.query(User.User).filter(User.User.id == uid).first()
#     return {
#             "user_id": uid,
#             "name": user.name,
#             "email": email
#             }



# app.include_router(router)
# origins = ["*"]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )
