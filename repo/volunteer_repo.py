# repo/volunteer_repo.py

import json
from datetime import datetime
from sqlalchemy.orm import Session
from models.user import User


def get_volunteers_by_emotions(db: Session, user_emotions: list, limit: int = 5):
    """
    Get available volunteers based on user's emotions keywords.
    Filters volunteers (users with role='volunteer') that:
    - Match user's emotions
    - Are currently available (availability_date is today or later and within time range)
    
    Args:
        db: Database session
        user_emotions: List of emotion keywords from user
        limit: Maximum number of volunteers to return (default 5)
    
    Returns:
        List of volunteers (up to limit) whose emotions match and are available
    """
    
    # Get all active volunteers
    volunteers = db.query(User).filter(
        User.role == "volunteer",
        User.is_active == True
    ).all()
    
    if not volunteers:
        return []
    
    # Parse emotions for each volunteer and filter by availability
    matching_volunteers = []
    current_time = datetime.utcnow()
    
    for volunteer in volunteers:
        # Check availability
        if volunteer.availability_date:
            # If availability_date is in the past, skip
            if volunteer.availability_date < current_time:
                continue
        
        try:
            volunteer_emotions = json.loads(volunteer.emotions_kw) if volunteer.emotions_kw else []
        except (json.JSONDecodeError, TypeError):
            volunteer_emotions = []
        
        # Check if volunteer has any matching emotions with user
        has_match = any(emotion in volunteer_emotions for emotion in user_emotions)
        
        if has_match or not user_emotions:  # Include if match or no user emotions
            matching_volunteers.append(volunteer)
    
    # Return first 'limit' volunteers
    return matching_volunteers[:limit]


def get_all_volunteers(db: Session, limit: int = 5):
    """
    Get all active volunteers with limit (no availability check for fallback).
    
    Args:
        db: Database session
        limit: Maximum number of volunteers to return
    
    Returns:
        List of volunteers up to limit
    """
    
    volunteers = db.query(User).filter(
        User.role == "volunteer",
        User.is_active == True,
    ).limit(limit).all()
    
    return volunteers


def get_all_volunteers_paginated(db: Session, skip: int = 0, limit: int = 10):
    """
    Get all active volunteers with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip (offset)
        limit: Maximum number of volunteers to return per page
    
    Returns:
        Tuple of (volunteers list, total count)
    """
    
    query = db.query(User).filter(
        User.role == "volunteer",
        User.is_active == True,
    )
    
    total = query.count()
    volunteers = query.offset(skip).limit(limit).all()
    
    return volunteers, total


def get_available_volunteers(db: Session, limit: int = 5):
    """
    Get all active volunteers that are available right now.
    Checks if current time is within availability_start_time and availability_end_time.
    
    Args:
        db: Database session
        limit: Maximum number of volunteers to return
    
    Returns:
        List of available volunteers up to limit
    """
    
    current_time = datetime.utcnow()
    current_date = current_time.date()
    current_time_only = current_time.time()
    
    volunteers = db.query(User).filter(
        User.role == "volunteer",
        User.is_active == True
    ).all()
    
    available = []
    
    for volunteer in volunteers:
        # Check if date matches today
        if volunteer.availability_date and volunteer.availability_date.date() != current_date:
            continue
        
        # Check if current time is within availability window
        if volunteer.availability_start_time and volunteer.availability_end_time:
            if volunteer.availability_start_time <= current_time_only <= volunteer.availability_end_time:
                available.append(volunteer)
        elif volunteer.availability_date:
            # If only date is set (no time range), consider available
            available.append(volunteer)
    
    return available[:limit]


def get_volunteer_by_id(db: Session, volunteer_id: int):
    """
    Get a single volunteer by ID.
    
    Args:
        db: Database session
        volunteer_id: Volunteer's user ID
    
    Returns:
        Volunteer user object or None
    """
    
    return db.query(User).filter(
        User.id == volunteer_id,
        User.role == "volunteer",
        User.is_active == True
    ).first()
