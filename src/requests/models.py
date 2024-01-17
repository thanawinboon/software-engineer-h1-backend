from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import date

from src.auth.models import User

class Request(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    leave_date: date
    leave_duration: int
    reason: str

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="requests")

