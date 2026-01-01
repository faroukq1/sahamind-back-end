import json
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.user import User
from passlib.hash import bcrypt
from core.security import hash_password

db: Session = SessionLocal()

new_user = User(
    email="farouk@gmail.com",
    password_hash=hash_password("aa"),
    role="benevole",
    emotions_kw=json.dumps(["anxiety", "stress", "burnout"]),
    is_active=True
)

db.add(new_user)
db.commit()
db.close()
