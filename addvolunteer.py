# addvolunteer.py
"""
Script to add a single volunteer to the database.
Usage: python addvolunteer.py
"""

from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.user import User
from core.security import hash_password
import json
from datetime import datetime, time, timedelta


def add_volunteer(email: str, emotions_kw: list, password: str = "volunteer123"):
    """
    Add a single volunteer to the database.
    
    Args:
        email: Volunteer email address
        emotions_kw: List of emotion keywords (e.g., ["anxiety", "stress"])
        password: Volunteer password (default: volunteer123)
    """
    
    db: Session = SessionLocal()
    
    try:
        print(f"🚀 Adding volunteer: {email}")
        print("="*50)
        
        # Check if volunteer already exists
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"⚠️  Volunteer with email {email} already exists!")
            return False
        
        # Create new volunteer
        volunteer = User(
            email=email,
            password_hash=hash_password(password),
            role="volunteer",
            emotions_kw=json.dumps(emotions_kw),  # Store as JSON string
            is_active=True,
            created_at=datetime.utcnow(),
        )
        
        db.add(volunteer)
        db.commit()
        
        print(f"✅ Successfully created volunteer!")
        print(f"   Email: {email}")
        print(f"   Emotions: {', '.join(emotions_kw)}")
        print(f"   Password: {password}")
        print("="*50)
        
        return True
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error adding volunteer: {str(e)}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    # Example usage - Add multiple volunteers
    volunteers_to_add = [
        {
            "email": "rachel.green@volunteer.com",
            "emotions_kw": ["loneliness", "isolation", "connection"],
            "availability_date": datetime.utcnow().date(),
            "start_time": time(9, 0),
            "end_time": time(12, 0),
        },
        {
            "email": "michael.scott@volunteer.com",
            "emotions_kw": ["confidence", "leadership", "motivation"],
            "availability_date": datetime.utcnow().date(),
            "start_time": time(14, 0),
            "end_time": time(17, 0),
        },
        {
            "email": "pam.beesly@volunteer.com",
            "emotions_kw": ["creativity", "joy", "happiness"],
            "availability_date": datetime.utcnow().date(),
            "start_time": time(10, 0),
            "end_time": time(13, 0),
        },
    ]
    
    print("\n🎯 Adding Volunteers to Database\n")
    
    for vol in volunteers_to_add:
        volunteer = User(
            email=vol["email"],
            password_hash=hash_password("volunteer123"),
            role="volunteer",
            emotions_kw=json.dumps(vol["emotions_kw"]),
            availability_date=datetime.combine(vol["availability_date"], time.min),
            availability_start_time=vol["start_time"],
            availability_end_time=vol["end_time"],
            is_active=True,
            created_at=datetime.utcnow(),
        )
        
        db: Session = SessionLocal()
        
        try:
            # Check if volunteer already exists
            existing = db.query(User).filter(User.email == vol["email"]).first()
            if existing:
                print(f"⚠️  Volunteer {vol['email']} already exists!")
                continue
            
            db.add(volunteer)
            db.commit()
            
            print(f"✅ Created volunteer: {vol['email']}")
            print(f"   - Emotions: {', '.join(vol['emotions_kw'])}")
            print(f"   - Available: {vol['availability_date']} ({vol['start_time'].strftime('%H:%M')} - {vol['end_time'].strftime('%H:%M')})\n")
        except Exception as e:
            db.rollback()
            print(f"❌ Error adding volunteer: {str(e)}\n")
        finally:
            db.close()
    
    print("\n✅ All volunteers processed!")
