from typing import List
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    password: str

    requests: List["Request"] = Relationship(back_populates="user")

