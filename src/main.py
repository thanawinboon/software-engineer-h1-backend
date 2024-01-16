from fastapi import FastAPI

from src.auth.router import router as auth_router

app = FastAPI()
app.include_router(auth_router, prefix="/auth")


@app.get("/")
def hello():
    return {"msg": "yay"}
