from pydantic import BaseModel
from datetime import date

class LeaveRequest(BaseModel):
    leave_date: date
    leave_duration: int

    reason: str