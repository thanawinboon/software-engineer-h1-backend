from typing import Optional
from datetime import datetime, timedelta

from sqlmodel import Session, select
from src.database.database import engine

from src.auth.models import User
from .models import Request
from .schemas import LeaveRequest

def create_request(user: User, leave_request: LeaveRequest) -> int:
    with Session(engine) as session:
        request = Request(
            leave_date=leave_request.leave_date,
            leave_duration=leave_request.leave_duration,
            reason=leave_request.reason,
            user=user
        )
        session.add(request)
        session.commit()
        session.refresh(request)
        return request

