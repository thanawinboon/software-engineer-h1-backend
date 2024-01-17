from fastapi import Depends, HTTPException, APIRouter

from src.auth.service import AuthHandler, get_user_by_id
from .schemas import LeaveRequest
from .service import create_request

router = APIRouter()
auth_handler = AuthHandler()

@router.post("/leave-request", status_code=201)
def request(request_details: LeaveRequest, user_id=Depends(auth_handler.auth_wrapper)):
    print(request_details)
    
    selected_user = get_user_by_id(user_id)
    if not selected_user:
        raise HTTPException(status_code=400, detail="User does not exist")
    
    if request_details.leave_duration < 1:
        raise HTTPException(status_code=400, detail="Leave duration should be at least 1 day")
    
    created_request = create_request(selected_user, request_details)
    return created_request