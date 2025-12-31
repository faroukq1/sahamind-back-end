from sqlalchemy.orm import Session
from models.journal import Journal

def create(db: Session, journal: Journal):
    db.add(journal)
    db.commit()
    db.refresh(journal)
    return journal


def get_by_user(db: Session, user_id: int):
    return db.query(Journal).filter(Journal.user_id == user_id).order_by(Journal.created_at.desc()).all()


def get_one(db: Session, journal_id: int):
    return db.query(Journal).filter(Journal.id == journal_id).first()


def delete(db: Session, journal: Journal):
    db.delete(journal)
    db.commit()


def update(db: Session):
    db.commit()
