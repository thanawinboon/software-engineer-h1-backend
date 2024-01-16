import os
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from passlib.context import CryptContext

# https://youtu.be/xZnOoO3ImSY?si=PSMb6FIW5YB39Dra
class AuthHandler():
    def __init__(self):
        load_dotenv()
        self.security = HTTPBearer()
        self.secret_key = os.environ.get("SECRET_KEY", "secret_12340987")
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.algorithm = os.environ.get("ALGORITHM", "HS256")

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def encode_token(self, user_id):
        payload = {
            "exp": datetime.utcnow() + timedelta(minutes=15),
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