# api/volunteer.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
import json
from models.user import User
from core.database import get_db
from repo import volunteer_repo
from schemas.volunteer import VolunteerResponse, VolunteerPaginatedResponse


router = APIRouter(prefix="/volunteers", tags=["volunteers"])


@router.get("/", response_model=List[VolunteerResponse])
def get_all_volunteers(db: Session = Depends(get_db)):
    """
    Get all active and available volunteers (limit 5).
    Only returns volunteers with future or today's availability_date.
    """
    volunteers = volunteer_repo.get_all_volunteers(db, limit=5)
    return volunteers


@router.get("/paginated", response_model=VolunteerPaginatedResponse)
def get_all_volunteers_paginated(
    page: int = Query(1, ge=1, description="Page number starting from 1"),
    page_size: int = Query(10, ge=1, le=50, description="Number of items per page"),
    db: Session = Depends(get_db)
):
    """
    Get all active volunteers with pagination.
    
    Args:
        page: Page number (starts at 1)
        page_size: Number of volunteers per page (default 10, max 50)
    
    Returns:
        Paginated list of volunteers with metadata
    """
    skip = (page - 1) * page_size
    volunteers, total = volunteer_repo.get_all_volunteers_paginated(db, skip=skip, limit=page_size)
    
    total_pages = (total + page_size - 1) // page_size  # Ceiling division
    
    return {
        "volunteers": volunteers,
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1
    }


@router.get("/available", response_model=List[VolunteerResponse])
def get_available_volunteers(db: Session = Depends(get_db)):
    """
    Get volunteers available RIGHT NOW.
    Checks if current time falls within their availability window.
    Returns up to 5 available volunteers.
    """
    volunteers = volunteer_repo.get_available_volunteers(db, limit=5)
    return volunteers


@router.get("/by-emotions/{user_id}", response_model=List[VolunteerResponse])
def get_volunteers_by_user_emotions(user_id: int, db: Session = Depends(get_db)):
    """
    Get volunteers matching the user's emotion keywords and are available.
    Fetches the user's emotions_kw and returns matching volunteers (limit 5).
    
    Args:
        user_id: ID of the user
    
    Returns:
        List of volunteers whose emotions match user's emotions and are available (up to 5)
    """
    
    # Get the user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Parse user's emotions
    try:
        user_emotions = json.loads(user.emotions_kw) if user.emotions_kw else []
    except (json.JSONDecodeError, TypeError):
        user_emotions = []
    
    # Get matching volunteers
    volunteers = volunteer_repo.get_volunteers_by_emotions(db, user_emotions, limit=5)
    
    return volunteers


@router.get("/{volunteer_id}", response_model=VolunteerResponse)
def get_volunteer_by_id(volunteer_id: int, db: Session = Depends(get_db)):
    """
    Get a single volunteer by ID with their availability details.
    
    Args:
        volunteer_id: Volunteer's user ID
    
    Returns:
        Volunteer details including availability
    """
    
    volunteer = volunteer_repo.get_volunteer_by_id(db, volunteer_id)
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    
    return volunteer
