# volunteer_seed.py
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.user import User
from core.security import hash_password
import json
from datetime import datetime, time, timedelta


def seed_volunteers():
    """Seed volunteer users with emotions_kw and scheduling info"""
    
    db: Session = SessionLocal()
    
    try:
        print("🚀 Running volunteers seed script...")
        print("="*50)
        
        # Check if volunteers already exist
        existing_volunteers = db.query(User).filter(User.role == "volunteer").count()
        if existing_volunteers > 0:
            print(f"⚠️  Found {existing_volunteers} existing volunteers. Clearing old volunteers...")
            db.query(User).filter(User.role == "volunteer").delete()
            db.commit()
        
        print("\n👥 Creating volunteers...")
        
        # Get today's date and tomorrow's date for availability
        today = datetime.utcnow().date()
        tomorrow = today + timedelta(days=1)
        
        # Volunteer data with emotions and availability
        volunteers_data = [
            {
                "email": "sarah.johnson@volunteer.com",
                "name": "Sarah Johnson",
                "emotions_kw": ["anxiety", "stress", "depression"],
                "availability": "Monday-Friday, 2:30 PM",
                "specialty": "Anxiety & Stress",
                "availability_date": today,
                "start_time": time(14, 30),  # 2:30 PM
                "end_time": time(17, 30),    # 5:30 PM
            },
            {
                "email": "ahmed.hassan@volunteer.com",
                "name": "Ahmed Hassan",
                "emotions_kw": ["depression", "mood", "sadness"],
                "availability": "Tuesday-Thursday, 4:00 PM",
                "specialty": "Depression & Mood",
                "availability_date": today,
                "start_time": time(16, 0),   # 4:00 PM
                "end_time": time(19, 0),     # 7:00 PM
            },
            {
                "email": "emily.chen@volunteer.com",
                "name": "Emily Chen",
                "emotions_kw": ["self-esteem", "confidence", "growth"],
                "availability": "Daily, 10:00 AM",
                "specialty": "Self-esteem & Growth",
                "availability_date": today,
                "start_time": time(10, 0),   # 10:00 AM
                "end_time": time(13, 0),     # 1:00 PM
            },
            {
                "email": "james.wilson@volunteer.com",
                "name": "James Wilson",
                "emotions_kw": ["anxiety", "panic", "fear"],
                "availability": "Monday-Wednesday, 6:00 PM",
                "specialty": "Anxiety & Panic",
                "availability_date": tomorrow,
                "start_time": time(18, 0),   # 6:00 PM
                "end_time": time(21, 0),     # 9:00 PM
            },
            {
                "email": "lisa.martinez@volunteer.com",
                "name": "Lisa Martinez",
                "emotions_kw": ["stress", "burnout", "exhaustion"],
                "availability": "Friday-Sunday, 3:00 PM",
                "specialty": "Stress & Burnout",
                "availability_date": today,
                "start_time": time(15, 0),   # 3:00 PM
                "end_time": time(18, 0),     # 6:00 PM
            },
        ]
        
        # Create volunteers
        for vol_data in volunteers_data:
            volunteer = User(
                email=vol_data["email"],
                password_hash=hash_password("volunteer123"),  # Default password
                role="volunteer",
                emotions_kw=json.dumps(vol_data["emotions_kw"]),  # Store as JSON string
                availability_date=datetime.combine(vol_data["availability_date"], time.min),
                availability_start_time=vol_data["start_time"],
                availability_end_time=vol_data["end_time"],
                is_active=True,
                created_at=datetime.utcnow(),
            )
            db.add(volunteer)
            print(f"✅ Created volunteer: {vol_data['email']}")
            print(f"   - Specialty: {vol_data['specialty']}")
            print(f"   - Emotions: {', '.join(vol_data['emotions_kw'])}")
            print(f"   - Availability: {vol_data['availability']}\n")
        
        db.commit()
        print("="*50)
        print(f"✅ Successfully seeded {len(volunteers_data)} volunteers!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding volunteers: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_volunteers()
