import fastapi as _fa
import uvicorn
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from src.database import database as _db
# from src.routes import router
import sqlalchemy.orm as _orm
from src.routes import sign_up, sign_in, sign_out, refresh_token
from src.models import users as User

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

# app.include_router(router)
# origins = ["*"]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )