# seed_journals.py
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.user import User
from models.journal import Journal
from datetime import datetime, timedelta


def seed_journals_for_user():
    """Seed journals for user_id = 1 with different colors and pin status"""
    
    db: Session = SessionLocal()
    
    try:
        print("🚀 Running journals seed script...")
        print("="*50)
        
        # Get user with ID 1
        user = db.query(User).filter(User.id == 1).first()
        
        if not user:
            print("❌ User with ID 1 not found!")
            return
        
        print(f"✅ Found user: {user.email}")
        
        # Check if journals already exist for this user
        existing_journals = db.query(Journal).filter(Journal.user_id == 1).count()
        if existing_journals > 0:
            print(f"⚠️  User already has {existing_journals} journals. Clearing old journals...")
            db.query(Journal).filter(Journal.user_id == 1).delete()
            db.commit()
        
        print("\n📔 Creating journals...")
        
        # Available colors for journals
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8", 
                  "#F7DC6F", "#BB8FCE", "#85C1E2", "#F8B88B", "#ABEBC6"]
        
        # =====================================================
        # PINNED JOURNALS (5 journals)
        # =====================================================
        
        pinned_journals = [
            Journal(
                user_id=1,
                title="My Journey to Better Mental Health",
                content="Today I realized that taking care of my mental health is just as important as physical health. I've started meditating for 10 minutes each morning, and I can already feel the difference. My anxiety levels have decreased, and I feel more centered throughout the day. It's amazing how such a small habit can have such a big impact.",
                humor="happy",
                color=colors[0],  # Red
                is_pinned=True,
                report=False,
                created_at=datetime.now() - timedelta(days=10),
                updated_at=datetime.now() - timedelta(days=10)
            ),
            Journal(
                user_id=1,
                title="Gratitude List - Things I'm Thankful For",
                content="🙏 Supportive family and friends\n🙏 Good health\n🙏 Opportunity to learn and grow\n🙏 A roof over my head\n🙏 Access to education\n🙏 Beautiful moments each day\n🙏 The ability to pursue my dreams\n\nReminding myself to be grateful for these blessings helps me stay positive.",
                humor="grateful",
                color=colors[1],  # Teal
                is_pinned=True,
                report=False,
                created_at=datetime.now() - timedelta(days=8),
                updated_at=datetime.now() - timedelta(days=5)
            ),
            Journal(
                user_id=1,
                title="Overcoming Exam Stress",
                content="Finals week has been incredibly challenging. I've been feeling overwhelmed with the workload, but I'm learning to break things down into smaller tasks. Today I managed to complete two study sessions using the Pomodoro technique. Taking breaks is actually helping me retain information better. I'm proud of myself for not giving up.",
                humor="anxious",
                color=colors[3],  # Orange
                is_pinned=True,
                report=False,
                created_at=datetime.now() - timedelta(days=7),
                updated_at=datetime.now() - timedelta(days=2)
            ),
            Journal(
                user_id=1,
                title="Daily Reflections & Growth",
                content="I've decided to make daily reflection a habit. Looking back at my day helps me understand my emotions better and identify patterns in my behavior. Today was productive - I accomplished my main goals and even had time to relax. Small wins matter, and I'm learning to celebrate them.",
                humor="calm",
                color=colors[6],  # Purple
                is_pinned=True,
                report=False,
                created_at=datetime.now() - timedelta(days=6),
                updated_at=datetime.now() - timedelta(days=1)
            ),
            Journal(
                user_id=1,
                title="Self-Care Reminders",
                content="💙 It's okay to take breaks\n💙 Progress over perfection\n💙 Be kind to yourself\n💙 Ask for help when needed\n💙 Your feelings are valid\n💙 Rest is productive\n💙 You're doing better than you think\n\nThese reminders help me on tough days.",
                humor="peaceful",
                color=colors[2],  # Blue
                is_pinned=True,
                report=False,
                created_at=datetime.now() - timedelta(days=5),
                updated_at=datetime.now()
            ),
        ]
        
        db.add_all(pinned_journals)
        db.flush()
        print(f"✅ Created 5 pinned journals")
        
        # =====================================================
        # UNPINNED JOURNALS (10 journals)
        # =====================================================
        
        unpinned_journals = [
            Journal(
                user_id=1,
                title="A Really Good Day",
                content="Today was one of those rare perfect days. Everything just clicked. I woke up feeling refreshed, had a great workout, aced my presentation at class, and even had time to catch up with old friends. These are the days I want to remember when times get tough. Life is good.",
                humor="joyful",
                color=colors[4],  # Green
                is_pinned=False,
                report=False,
                created_at=datetime.now() - timedelta(days=9),
                updated_at=datetime.now() - timedelta(days=9)
            ),
            Journal(
                user_id=1,
                title="Dealing with Disappointment",
                content="Didn't get the internship I applied for. It stings, not going to lie. But I know this isn't the end. Maybe it's a redirection to something better. I'll take this as a learning experience, work on improving my skills, and try again. Rejection is part of the journey.",
                humor="sad",
                color=colors[5],  # Yellow
                is_pinned=False,
                report=False,
                created_at=datetime.now() - timedelta(days=8),
                updated_at=datetime.now() - timedelta(days=7)
            ),
            Journal(
                user_id=1,
                title="Feeling Stuck",
                content="Lately I've been feeling like I'm not making progress. Watching everyone else succeed on social media doesn't help. But I need to remind myself that everyone's journey is different and I'm comparing my behind-the-scenes to everyone else's highlight reel. I need to focus on my own path.",
                humor="frustrated",
                color=colors[9],  # Light green
                is_pinned=False,
                report=False,
                created_at=datetime.now() - timedelta(days=4),
                updated_at=datetime.now() - timedelta(days=3)
            ),
            Journal(
                user_id=1,
                title="Breakthrough Moment",
                content="Finally understood that concept I've been struggling with for weeks! The feeling of something clicking into place is incredible. Sometimes you just need to step away and come back with fresh eyes. This is why persistence matters. So proud of myself right now!",
                humor="excited",
                color=colors[7],  # Light blue
                is_pinned=False,
                report=False,
                created_at=datetime.now() - timedelta(days=12),
                updated_at=datetime.now() - timedelta(days=11)
            ),
            Journal(
                user_id=1,
                title="Sunday Reset",
                content="Spent today doing a full reset - cleaned my room, meal prepped for the week, organized my study schedule, and had a long relaxing bath. There's something therapeutic about starting fresh. I feel ready to tackle whatever this week brings. Sunday self-care is essential.",
                humor="content",
                color=colors[0],  # Red
                is_pinned=False,
                report=False,
                created_at=datetime.now() - timedelta(days=6),
                updated_at=datetime.now() - timedelta(days=4)
            ),
            Journal(
                user_id=1,
                title="Unexpected Kindness",
                content="A stranger at the coffee shop paid for my drink today when they saw I forgot my wallet. Such a small gesture but it completely brightened my day. It reminded me that there's still so much good in the world. I'm definitely paying it forward soon.",
                humor="touched",
                color=colors[2],  # Blue
                is_pinned=False,
                report=False,
                created_at=datetime.now() - timedelta(days=15),
                updated_at=datetime.now() - timedelta(days=14)
            ),
            Journal(
                user_id=1,
                title="Late Night Thoughts",
                content="Can't sleep. Mind racing with thoughts about the future. What if I'm not good enough? What if I fail? But also - what if everything works out better than I imagined? I need to give myself credit for how far I've already come. Tomorrow is a new day.",
                humor="worried",
                color=colors[8],  # Peach
                is_pinned=False,
                report=False,
                created_at=datetime.now() - timedelta(days=3),
                updated_at=datetime.now() - timedelta(days=2)
            ),
            Journal(
                user_id=1,
                title="Family Time",
                content="Had dinner with family today. No phones, just conversation and laughter. I forget how important these moments are when I get caught up in my busy routine. They reminded me that I always have a support system, no matter what. Feeling grateful and loved.",
                humor="loved",
                color=colors[5],  # Yellow
                is_pinned=False,
                report=False,
                created_at=datetime.now() - timedelta(days=20),
                updated_at=datetime.now() - timedelta(days=18)
            ),
            Journal(
                user_id=1,
                title="Processing Change",
                content="Change is scary but also exciting. I'm learning to embrace uncertainty instead of fighting it. Not everything needs to be planned out. Sometimes the best experiences come from spontaneous decisions. I'm growing, evolving, and that's okay.",
                humor="hopeful",
                color=colors[6],  # Purple
                is_pinned=False,
                report=False,
                created_at=datetime.now() - timedelta(hours=5),
                updated_at=datetime.now() - timedelta(hours=5)
            ),
            Journal(
                user_id=1,
                title="Lessons from Today",
                content="What I learned: 1) It's okay to say no, 2) Boundaries are healthy, 3) My time is valuable, 4) I don't have to explain myself to everyone. Setting boundaries felt uncomfortable at first, but it's necessary for my wellbeing. Self-respect matters.",
                humor="empowered",
                color=colors[1],  # Teal
                is_pinned=False,
                report=False,
                created_at=datetime.now() - timedelta(days=25),
                updated_at=datetime.now() - timedelta(days=24)
            ),
        ]
        
        db.add_all(unpinned_journals)
        db.flush()
        print(f"✅ Created 10 unpinned journals")
        
        # =====================================================
        # COMMIT ALL CHANGES
        # =====================================================
        
        db.commit()
        
        print("\n" + "="*50)
        print("✅ Journals seeding completed successfully!")
        print("="*50)
        print(f"📊 Summary:")
        print(f"   - User: {user.email} (ID: {user.id})")
        print(f"   - 5 Pinned journals created")
        print(f"   - 10 Unpinned journals created")
        print(f"   - Total: 15 journals")
        print(f"\n🎨 Colors used:")
        print(f"   - Red, Teal, Blue, Orange, Green")
        print(f"   - Yellow, Purple, Light Blue, Peach, Light Green")
        print(f"\n😊 Humors included:")
        print(f"   - happy, grateful, anxious, calm, peaceful")
        print(f"   - joyful, sad, frustrated, excited, content")
        print(f"   - touched, worried, loved, hopeful, empowered")
        print("="*50 + "\n")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_journals_for_user()
