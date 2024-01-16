from fastapi import Depends, HTTPException, APIRouter, Request

from .schemas import AuthDetails
from .service import AuthHandler

router = APIRouter()
auth_handler = AuthHandler()

@router.post("/register", status_code=201)
def register(auth_details: AuthDetails):
    print(auth_details.username, auth_details.password)
    
    # TODO: check db for existing username here

    hashed_password = auth_handler.get_password_hash(auth_details.password)

    # TODO: add user into db here

    user = { "username": "fake", "password": "abc" }

    token = auth_handler.encode_token(user["id"])
    return token


@router.post("/login")
def login(auth_details: AuthDetails):

    # TODO: get user from db by username here
    user = { "username": "fake", "password": "abc" }

    if (not user) or (not auth_handler.verify_password(auth_details.password, user["password"])):
        raise HTTPException(status_code=401, detail="Invalid username and/or password")
    token = auth_handler.encode_token(user["id"])
    return token



@router.get('/unprotected')
def unprotected():
    return { 'hello': 'world' }

@router.get('/protected')
def protected(username=Depends(auth_handler.auth_wrapper)):
    return { 'name': username }