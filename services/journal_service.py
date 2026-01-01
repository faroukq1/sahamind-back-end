# services/journal_service.py
from sqlalchemy.orm import Session
from models.journal import Journal
from schemas.journal import JournalCreate, JournalUpdate
from repo import journal_repo
from sqlalchemy import func


def add_note(db: Session, user_id: int, data: JournalCreate):
    """Create a new journal entry"""
    journal = Journal(
        user_id=user_id,
        humor=data.humor,
        title=data.title,
        content=data.content,
        is_pinned=data.is_pinned,  # Add this
        color=data.color  # Add this
    )
    return journal_repo.create(db, journal)


def get_user_notes(db: Session, user_id: int):
    """Get all notes for a user (ordered by pinned first)"""
    return journal_repo.get_by_user(db, user_id)


def get_pinned_notes(db: Session, user_id: int):
    """Get only pinned notes for a user"""
    return (
        db.query(Journal)
        .filter(Journal.user_id == user_id, Journal.is_pinned == True)
        .order_by(Journal.created_at.desc())
        .all()
    )


def delete_note(db: Session, journal_id: int):
    """Delete a journal entry"""
    journal = journal_repo.get_one(db, journal_id)
    if not journal:
        return False

    journal_repo.delete(db, journal)
    return True


def update_note(db: Session, journal_id: int, data: JournalUpdate):
    """Update a journal entry"""
    journal = journal_repo.get_one(db, journal_id)
    if not journal:
        return None

    for field, value in data.dict(exclude_unset=True).items():
        setattr(journal, field, value)

    journal_repo.update(db)
    return journal


def toggle_pin(db: Session, journal_id: int):
    """Toggle pin status of a note"""
    journal = journal_repo.get_one(db, journal_id)
    if not journal:
        return None
    
    journal.is_pinned = not journal.is_pinned
    journal_repo.update(db)
    return journal


def update_color(db: Session, journal_id: int, color: str):
    """Update the color of a note"""
    journal = journal_repo.get_one(db, journal_id)
    if not journal:
        return None
    
    journal.color = color
    journal_repo.update(db)
    return journal

# services/journal_service.py
def get_note_by_id(db: Session, journal_id: int):
    """Get a single journal entry by ID"""
    return db.query(Journal).filter(Journal.id == journal_id).first()


def humor_report(db: Session, user_id: int):
    """Generate humor statistics grouped by date"""
    rows = (
        db.query(
            Journal.humor,
            func.date(Journal.created_at),
            func.count(Journal.id)
        )
        .filter(Journal.user_id == user_id)
        .group_by(Journal.humor, func.date(Journal.created_at))
        .order_by(func.date(Journal.created_at))
        .all()
    )

    report = {}
    for humor, date, count in rows:
        report.setdefault(humor, []).append({
            "date": str(date),
            "count": count
        })

    return report
