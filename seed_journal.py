# seed_journal.py
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.journal import Journal
from models.user import User
import random
from datetime import datetime, timedelta

# Sample data
HUMORS = ["happy", "sad", "anxious", "calm", "excited", "neutral", "motivated", "tired", "grateful", "stressed"]

COLORS = [
    "#ffffff", "#fff9c4", "#ffe0b2", "#f8bbd0", "#d1c4e9", 
    "#e1f5fe", "#b2ebf2", "#c8e6c9", "#e6ee9c", "#ffccbc",
]

TITLES = [
    "Morning Reflections", "Project Ideas", "Grocery List", "Book Notes",
    "Workout Plan", "Travel Ideas 2026", "Meeting Notes", "Daily Goals",
    "Recipe to Try", "Movie Recommendations", "Birthday Gift Ideas",
    "Learning Notes", "Weekend Plans", "Important Reminders",
    "Inspiration Quotes", "Dream Journal", "Gratitude List",
    "Creative Ideas", "Future Plans", None,
]

CONTENTS = [
    "Started the day with meditation. Feeling grateful for the peaceful morning.",
    "Build a journaling app with React Native.\n• Pins and tags\n• Mood tracking",
    "☐ Milk\n☐ Eggs\n☐ Bread\n☐ Vegetables\n☐ Fruits",
    "Atomic Habits - James Clear\n\nKey: Small changes = Big results",
    "Monday: Chest & Triceps\nWednesday: Back & Biceps\nFriday: Legs",
    "🌸 Japan - cherry blossoms\n✨ Iceland - northern lights\n🕌 Morocco",
    "Discussed Q1 goals and new features for the app.",
    "1. Wake up at 6 AM\n2. Exercise for 30 minutes\n3. Read for 1 hour",
    "Chicken Curry Recipe:\n- 500g chicken\n- Curry paste\n- Coconut milk",
    "Must watch:\n• The Shawshank Redemption\n• Inception\n• Interstellar",
    "Mom: Gardening tools 🌱\nDad: Book 📚\nSister: Art supplies 🎨",
    "Python Tips:\n- List comprehensions\n- Type hints\n- F-strings",
    "Saturday: Farmers market, hiking\nSunday: Brunch, movie marathon",
    "📌 Dentist appointment Tuesday\n📌 Pay bills by Friday",
    "\"The only way to do great work is to love what you do.\" - Steve Jobs",
    "Dreamed about flying over mountains. Colors were vivid.",
    "Today I'm grateful for:\n🙏 Health\n🙏 Friends\n🙏 Opportunities",
    "💡 App idea: Social platform\n💡 Blog topic: Mental health",
    "5-year plan:\n- Build business\n- Travel to 10 countries",
    "Remember to call dentist 📞",
]


def seed_journals(user_id: int = 2, count: int = 20):
    """Seed database with journal entries"""
    db = SessionLocal()
    
    try:
        # REMOVE USER CHECK - Just create journals directly
        print(f"🌱 Seeding {count} journals for user_id={user_id}...")
        
        created_journals = []
        
        for i in range(count):
            # Random date in the last 30 days
            days_ago = random.randint(0, 30)
            hours_ago = random.randint(0, 23)
            created_at = datetime.now() - timedelta(days=days_ago, hours=hours_ago)
            
            # 30% chance to be pinned
            is_pinned = random.random() < 0.3
            
            # Random title and content
            title = random.choice(TITLES)
            content = random.choice(CONTENTS)
            
            journal = Journal(
                user_id=user_id,
                humor=random.choice(HUMORS),
                title=title,
                content=content,
                is_pinned=is_pinned,
                color=random.choice(COLORS),
                report=False,
                created_at=created_at,
                updated_at=created_at
            )
            
            db.add(journal)
            created_journals.append(journal)
        
        db.commit()
        
        print(f"✅ Successfully created {count} journal entries!")
        print(f"📌 Pinned: {sum(1 for j in created_journals if j.is_pinned)}")
        print(f"📝 Unpinned: {sum(1 for j in created_journals if not j.is_pinned)}")
        
        # Verify
        total = db.query(Journal).filter(Journal.user_id == user_id).count()
        print(f"📊 Total journals in database for user_id={user_id}: {total}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_journals(user_id=1, count=20)
