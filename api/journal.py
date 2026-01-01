# routes/journal.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.journal import JournalCreate, JournalUpdate, JournalOut
from services import journal_service
from typing import List

router = APIRouter(prefix="/journals", tags=["Journals"])

@router.post("/", response_model=JournalOut)
def add_journal(user_id: int, data: JournalCreate, db: Session = Depends(get_db)):
    """Create a new journal entry"""
    return journal_service.add_note(db, user_id, data)

@router.get("/", response_model=List[JournalOut])
def get_journals(user_id: int, db: Session = Depends(get_db)):
    """Get all journals for a user"""
    return journal_service.get_user_notes(db, user_id)

@router.get("/pinned", response_model=List[JournalOut])
def get_pinned_journals(user_id: int, db: Session = Depends(get_db)):
    """Get only pinned journals"""
    return journal_service.get_pinned_notes(db, user_id)

# NEW ROUTE: Get single journal by ID
@router.get("/{journal_id}", response_model=JournalOut)
def get_journal_by_id(journal_id: int, db: Session = Depends(get_db)):
    """Get a single journal entry by ID"""
    journal = journal_service.get_note_by_id(db, journal_id)
    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found")
    return journal

@router.patch("/{journal_id}", response_model=JournalOut)
def update_journal(journal_id: int, data: JournalUpdate, db: Session = Depends(get_db)):
    """Update a journal entry"""
    journal = journal_service.update_note(db, journal_id, data)
    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found")
    return journal

@router.patch("/{journal_id}/pin", response_model=JournalOut)
def toggle_journal_pin(journal_id: int, db: Session = Depends(get_db)):
    """Toggle pin status"""
    journal = journal_service.toggle_pin(db, journal_id)
    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found")
    return journal

@router.patch("/{journal_id}/color", response_model=JournalOut)
def update_journal_color(journal_id: int, color: str, db: Session = Depends(get_db)):
    """Update journal color"""
    journal = journal_service.update_color(db, journal_id, color)
    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found")
    return journal

@router.delete("/{journal_id}")
def delete_journal(journal_id: int, db: Session = Depends(get_db)):
    """Delete a journal entry"""
    ok = journal_service.delete_note(db, journal_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Journal not found")
    return {"deleted": True}

@router.get("/report/humor")
def humor_stats(user_id: int, db: Session = Depends(get_db)):
    """Get humor statistics"""
    return journal_service.humor_report(db, user_id)
