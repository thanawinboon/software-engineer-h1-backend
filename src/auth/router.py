from fastapi import HTTPException, APIRouter

from .schemas import AuthDetails
from .service import AuthHandler, get_user, create_user

router = APIRouter()
auth_handler = AuthHandler()

@router.post("/register", status_code=201)
def register(auth_details: AuthDetails):
    print(auth_details.username, auth_details.password)
    
    selected_user = get_user(auth_details.username)
    if selected_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    user_id = create_user(auth_details.username, hashed_password)

    token = auth_handler.encode_token(user_id)
    return token


@router.post("/login", status_code=200)
def login(auth_details: AuthDetails):
    user = get_user(auth_details.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username")
    
    password_is_valid = auth_handler.verify_password(auth_details.password, user.password)
    if (not password_is_valid):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    token = auth_handler.encode_token(user.id)
    return token
