import json
from sqlalchemy.orm import Session
from models.user import User

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(
    db: Session,
    email: str,
    password_hash: str,
    emotions_kw: list[str]
):
    user = User(
        email=email,
        password_hash=password_hash,
        role="patient",
        emotions_kw=json.dumps(emotions_kw)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
