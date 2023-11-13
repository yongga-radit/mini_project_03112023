import fastapi as _fa
import uvicorn
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from src.database import database as _db
# from src.routes import router
import sqlalchemy.orm as _orm
from src.routes import sign_up, sign_in, sign_out, refresh_token, update_data, order
from src.models import users as User, book_stocks as _bs
from src.depends import authentication as _auth


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
   data: sign_out.LogoutData, 
   db: Session = _fa.Depends(_db.get_db)
):
    return await sign_out.signout(data=data, db=db)


@app.post("/user/refresh-token", tags=["Users"])
async def token(
   data: refresh_token.RefreshToken, 
   db: Session = _fa.Depends(_db.get_db)
):
    return await refresh_token.refresh_token(data=data, db=db)


@app.post("/user/info", tags=["Users"])
async def update_user(
   data: update_data.UpdateUserInfo, 
   db: Session = _fa.Depends(_db.get_db)
):
    return await update_data.update_info(data=data, db=db)


# ------------------ BOOKS LOAN -----------------------------
@app.post("/books/register", tags=['Books'])
async def create_book(
   data: order.RegisterProduct,
#    payload: _fa.Depends(_auth.Authentication()),
   db: Session = _fa.Depends(_db.get_db)
):
    return await order.register_book(data=data, payload=_fa.Depends(_auth.Authentication()), db=db)


@app.post("/books/order", tags=["Books"])
async def loaned_books(
    data: order.OrderInput,
    # payload = _fa.Depends(_auth.Authentication()),
    db: Session = _fa.Depends(_db.get_db)
):
    return await order.order(data=data, db=db)


@app.get("/books/return", tags=["Books"])
async def return_books(
    data: order.ReturnBook,
    payload = _fa.Depends(_auth.Authentication()),
    db: Session = _fa.Depends(_db.get_db)
):
    return await order.return_book(data=data, payload=payload, db=db)


# @app.get("/books/delete", tags=["Books"], response_model=_bs.Books)
# async def delete_books(
#     book_id: int,
#     payload = _fa.Depends(_auth.Authentication()),
#     db: Session = _fa.Depends(_db.get_db)
# ):
#     user_id = payload.get('uid', 0)
#     if user_id.user_role != 1:  # if not admin
#         _fa.HTTPException('Delete data only by Admin')

#     book = db.query(_bs.Books).filter(_bs.Books.id == book_id).first()

#     if not book:
#         _fa.HTTPException('Book not found')
    
#     db.delete(book)
#     db.commit()

#     return _fa.Response(status_code=200)


# app.include_router(router)
# origins = ["*"]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )
