# repo/journal_repo.py
from sqlalchemy.orm import Session
from models.journal import Journal


def create(db: Session, journal: Journal):
    """Create a new journal entry"""
    db.add(journal)
    db.commit()
    db.refresh(journal)
    return journal


def get_by_user(db: Session, user_id: int):
    """Get all journals for user, ordered by pinned first then date"""
    return (
        db.query(Journal)
        .filter(Journal.user_id == user_id)
        .order_by(Journal.is_pinned.desc(), Journal.created_at.desc())
        .all()
    )


def get_one(db: Session, journal_id: int):
    """Get a single journal by ID"""
    return db.query(Journal).filter(Journal.id == journal_id).first()


def delete(db: Session, journal: Journal):
    """Delete a journal entry"""
    db.delete(journal)
    db.commit()


def update(db: Session):
    """Commit changes to database"""
    db.commit()
