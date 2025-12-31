from sqlalchemy.orm import Session
from models.journal import Journal
from schemas.journal import JournalCreate, JournalUpdate
from repo import journal_repo
from sqlalchemy import func


def add_note(db: Session, user_id: int, data: JournalCreate):
    journal = Journal(
        user_id=user_id,
        humor=data.humor,
        title=data.title,
        content=data.content
    )
    return journal_repo.create(db, journal)



def get_user_notes(db: Session, user_id: int):
    return journal_repo.get_by_user(db, user_id)



def delete_note(db: Session, journal_id: int):
    journal = journal_repo.get_one(db, journal_id)
    if not journal:
        return False

    journal_repo.delete(db, journal)
    return True


def update_note(db: Session, journal_id: int, data: JournalUpdate):
    journal = journal_repo.get_one(db, journal_id)
    if not journal:
        return None

    for field, value in data.dict(exclude_unset=True).items():
        setattr(journal, field, value)

    journal_repo.update(db)
    return journal


def humor_report(db: Session, user_id: int):
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

