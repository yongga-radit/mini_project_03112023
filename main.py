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
from src.models import users as User, book_stocks as _bs
from src.depends import authentication as _auth, authorization as _author
from src.config import config as _config
from src.utils.encryption import validate_token


# creating database
_db.create_database()

# run the program
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


@app.post("/user/sign-up", tags=["Users"])
async def registration(
   data: sign_up.RegisterData,
   db: Session = _fa.Depends(_db.get_db)
):
    return await sign_up.signup(data=data, db=db)


@app.post("/user/sign-in", tags=["Users"])
async def login(
    data: sign_in.LoginData,
    db: Session = _fa.Depends(_db.get_db)
):
    return await sign_in.signin(data=data, db=db)


@app.post("/user/sign-out", tags=["Users"])
async def logout(
    # access_token: str,
    db: Session = _fa.Depends(_db.get_db),
    payload: dict = _fa.Depends(validate_token)
):
    return await sign_out.signout(payload=payload, db=db)


# @app.post("/user/refresh-token", tags=["Users"])
# async def token(
#    data: refresh_token.RefreshToken, 
#    db: Session = _fa.Depends(_db.get_db)
# ):
#     return await refresh_token.refresh_token(data=data, db=db)


@app.post("/user/info", tags=["Users"])
async def update_user(
   data: update_data.UpdateUserInfo, 
   payload: dict = _fa.Depends(validate_token),
   db: Session = _fa.Depends(_db.get_db)
):
    return await update_data.update_info(data=data, payload=payload, db=db)

@app.post("/user/reset/password", tags=["User"])
async def reset_password(
    data: update_data.UpdatePassword,
    payload: dict = _fa.Depends(validate_token),
    db: Session = _fa.Depends(_db.get_db)
):
    return await update_data.update_password(data=data, payload=payload, db=db)


# ------------------ VALIDATE TOKEN -----------------------------
@app.get("/token/validate", tags=["token"])
async def validate_access_token(
    payload: dict = _fa.Depends(validate_token),
    db: Session = _fa.Depends(_db.get_db)
) -> dict:
    uid = payload.get('uid', '')
    email = payload.get('email', '')
    user = db.query(User.User).filter(User.User.id == uid).first()
    return {
            "user_id": uid,
            "name": user.name,
            "email": email
            }


# ------------------ BOOKS LOAN -----------------------------
@app.post("/books/register", tags=['Books'])
async def create_book(
   data: add_product.RegisterProduct,
   payload: dict = _fa.Depends(validate_token),
   db: Session = _fa.Depends(_db.get_db)
):
    return await add_product.register_book(data=data, payload=payload, db=db)


@app.post("/books/order", tags=["Books"])
async def loaned_books(
    book_id: int,
    amount: int = 1,
    payload: dict = _fa.Depends(validate_token),
    db: Session = _fa.Depends(_db.get_db)
):
    return await order.order(book_id=book_id, amount=amount, payload=payload, db=db)


@app.get("/books/check-status", tags=["Books"])
async def check_status(
    loan_id: Optional[int],
    payload: dict = _fa.Depends(validate_token),
    db: Session = _fa.Depends(_db.get_db)
):
    return await submit.check_status(loan_id=loan_id, payload=payload, db=db)


@app.put("/books/post", tags=["Books"])
async def post_loan(
    loan_id: int,
    is_confirmed: bool = True,
    payload: dict = _fa.Depends(validate_token),
    db: Session = _fa.Depends(_db.get_db)
):
    return await submit.post(
                    loan_id=loan_id,
                    is_confirmed=is_confirmed,
                    payload=payload,
                    db=db
                )


@app.put("/books/return", tags=["Books"])
async def return_books(
    loan_id: int,
    fine_per_day: float,
    # return_date: datetime.date = datetime(2023, 12, 10),
    payload: dict = _fa.Depends(validate_token),
    db: Session = _fa.Depends(_db.get_db)
):
    return await update.return_book(loan_id=loan_id, fine_per_day=fine_per_day, payload=payload, db=db)


@app.delete("/books/delete", tags=["Books"])
async def delete_books(
    book_id: int,
    payload: dict = _fa.Depends(validate_token),
    db: Session = _fa.Depends(_db.get_db)
):
    # user_id = payload.get('uid', 0)
    # if user_id.user_role != 1:  # if not admin
    #     raise _fa.HTTPException('Delete data only by Admin')

    # book = db.query(_bs.Books).filter(_bs.Books.id == book_id).first()

    # if not book:
    #     raise _fa.HTTPException('Book not found')
    
    # db.delete(book)
    # db.commit()
    return await delete.delete_product(book_id=book_id, payload=payload, db=db)

@app.delete("/books/loan-delete", tags=["Books"])
async def delete_loan(
    loan_id: int,
    payload: dict = _fa.Depends(validate_token),
    db: Session = _fa.Depends(_db.get_db)
):
    return await delete.delete_loan(loan_id=loan_id, payload=payload, db=db)

# app.include_router(router)
# origins = ["*"]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )
