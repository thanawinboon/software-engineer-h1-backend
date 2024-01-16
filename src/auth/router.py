from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/temp")
def temp(request: Request):
    return {"msg": "yay"}

