from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.auth import UserCreate, UserLogin
from services.auth_service import signup, login
from core.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def signup_route(data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = signup(
            db,
            data.email,
            data.password,
            data.emotions_kw
        )
        return {"message": "Account created", "user_id": user.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login_route(data: UserLogin, db: Session = Depends(get_db)):
    try:
        data = login(db, data.email, data.password)
        return data
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
