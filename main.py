import fastapi as _fa
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from src.database import database as _db
from src.routes import router

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

app.include_router(router)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)