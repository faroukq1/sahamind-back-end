# scripts/create_test_forum.py
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from core.database import SessionLocal, engine, Base
from models.user import User
from models.forum import Forum, ForumModerator
from core.security import hash_password
import json

def create_test_data():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if users exist, if not create them
        user1 = db.query(User).filter(User.id == 1).first()
        if not user1:
            user1 = User(
                id=1,
                email="patient1@example.com",
                password_hash=hash_password("password123"),
                role="patient",
                emotions_kw=json.dumps(["anxiety", "stress"])
            )
            db.add(user1)
            print("✓ Created User 1 (Patient)")
        else:
            print("✓ User 1 already exists")
        
        user2 = db.query(User).filter(User.id == 2).first()
        if not user2:
            user2 = User(
                id=2,
                email="moderator1@example.com",
                password_hash=hash_password("password123"),
                role="volunteer",
                emotions_kw=json.dumps(["burnout", "stress", "anxiety"])
            )
            db.add(user2)
            print("✓ Created User 2 (Moderator)")
        else:
            print("✓ User 2 already exists")
        
        db.commit()
        
        # Check if forum exists
        forum = db.query(Forum).filter(Forum.name == "student_burnout").first()
        if not forum:
            # Create the forum
            forum = Forum(
                name="student_burnout",
                description="A safe space for students experiencing burnout to share and support each other",
                thematic="Academic Stress"
            )
            db.add(forum)
            db.flush()
            
            # Add moderator
            moderator = ForumModerator(
                forum_id=forum.id,
                user_id=2
            )
            db.add(moderator)
            db.commit()
            
            print(f"✓ Created forum 'student_burnout' with ID: {forum.id}")
            print(f"✓ Added User 2 as moderator")
        else:
            print(f"✓ Forum 'student_burnout' already exists with ID: {forum.id}")
        
        print("\n=== Test Data Created Successfully ===")
        print(f"Forum ID: {forum.id}")
        print(f"Patient User ID: 1")
        print(f"Moderator User ID: 2")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()