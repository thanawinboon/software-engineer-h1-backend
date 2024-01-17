from fastapi import FastAPI

from src.auth.router import router as auth_router
from src.requests.router import router as requests_router
from src.database.database import create_db_and_tables

app = FastAPI()
app.include_router(auth_router, prefix="/auth")
app.include_router(requests_router)

create_db_and_tables()

@app.get("/")
def hello():
    return {"msg": "yay"}
