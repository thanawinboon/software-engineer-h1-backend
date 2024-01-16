from sqlmodel import SQLModel, Field, Session, select
from src.database.database import engine

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    password: str

def get_user(username: str) -> User:
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        return session.exec(statement).one()

def create_user(username: str, password: str) -> int:
    user = User(username=username, password=password)
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user.id

