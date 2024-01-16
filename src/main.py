from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from src.auth.router import router as auth_router

app = FastAPI()
app.include_router(auth_router, prefix="/auth")


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 Password Bearer Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/helloworld")
def hello():
    return {"msg": "yay"}
