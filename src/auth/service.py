import os
import jwt
from typing import Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv

from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from sqlmodel import Session, select
from src.database.database import engine

from passlib.context import CryptContext

from .models import User

# https://youtu.be/xZnOoO3ImSY?si=PSMb6FIW5YB39Dra
class AuthHandler():
    security = HTTPBearer()
    def __init__(self):
        load_dotenv()
        self.secret_key = os.environ.get("SECRET_KEY", "secret_12340987")
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.algorithm = os.environ.get("ALGORITHM", "HS256")
        self.token_expiry_time_minutes = int(os.environ.get("TOKEN_EXPIRY_TIME_MINUTES", 15))

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def encode_token(self, user_id):
        payload = {
            "exp": datetime.utcnow() + timedelta(minutes=self.token_expiry_time_minutes),
            "iat": datetime.utcnow(),
            "sub": user_id
        }
        return jwt.encode(payload, self.secret_key, self.algorithm)
    
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, self.algorithm)
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Signature has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
    
    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)


def get_user(username: str) -> Optional[User]:
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        return session.exec(statement).first()

def create_user(username: str, password: str) -> int:
    user = User(username=username, password=password)
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user.id

