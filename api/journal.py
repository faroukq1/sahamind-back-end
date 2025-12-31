from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.journal import JournalCreate, JournalUpdate, JournalOut
from services import journal_service
from typing import List

router = APIRouter(prefix="/journals", tags=["Journals"])

@router.post("/", response_model=JournalOut)
def add_journal(user_id: int, data: JournalCreate, db: Session = Depends(get_db)):
    return journal_service.add_note(db, user_id, data)


@router.get("/", response_model=List[JournalOut])
def get_journals(user_id: int, db: Session = Depends(get_db)):
    return journal_service.get_user_notes(db, user_id)


@router.patch("/{journal_id}", response_model=JournalOut)
def update_journal(journal_id: int, data: JournalUpdate, db: Session = Depends(get_db)):
    journal = journal_service.update_note(db, journal_id, data)
    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found")
    return journal

@router.delete("/{journal_id}")
def delete_journal(journal_id: int, db: Session = Depends(get_db)):
    ok = journal_service.delete_note(db, journal_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Journal not found")
    return {"deleted": True}

@router.get("/report/humor")
def humor_stats(user_id: int, db: Session = Depends(get_db)):
    return journal_service.humor_report(db, user_id)

