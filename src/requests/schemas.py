from pydantic import BaseModel
from datetime import datetime

class LeaveRequest(BaseModel):
    leave_date: datetime
    leave_duration: int

    reason: str