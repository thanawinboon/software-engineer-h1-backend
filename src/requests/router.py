from fastapi import Depends, HTTPException, APIRouter

from src.auth.service import AuthHandler, get_user_by_id
from .schemas import LeaveRequest
from .service import create_request, list_request

router = APIRouter()
auth_handler = AuthHandler()

@router.get("/list", status_code=200)
def view_requests(user_id=Depends(auth_handler.auth_wrapper)):
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    return list_request()

@router.post("/send", status_code=201)
def make_request(request_details: LeaveRequest, user_id=Depends(auth_handler.auth_wrapper)):
    selected_user = get_user_by_id(user_id)
    if not selected_user:
        print("User does not exist")
        raise HTTPException(status_code=400, detail="User does not exist")
    
    if request_details.leave_duration < 1:
        print("Leave duration should be at least 1 day")
        raise HTTPException(status_code=400, detail="Leave duration should be at least 1 day")
    
    created_request = create_request(selected_user, request_details)
    return created_request