from sqlalchemy.orm import Session
from repo.user_repo import get_user_by_email, create_user
from core.security import hash_password, verify_password

def signup(db: Session, email: str, password: str, emotions_kw: list[str]):
    if get_user_by_email(db, email):
        raise ValueError("Email already registered")

    hashed = hash_password(password)
    return create_user(db, email, hashed, emotions_kw)


def login(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user or not verify_password(password, user.password_hash):
        raise ValueError("Invalid credentials")



    return user
