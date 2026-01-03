# seed_forums.py
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.user import User
from models.forum import Forum, Post, Response, PostLike, ResponseLike, ForumModerator
from core.security import hash_password
from datetime import datetime, timedelta


def seed_forums_and_posts():
    """Seed forums with posts and responses"""
    
    db: Session = SessionLocal()
    
    try:
        print("🚀 Running forums seed script...")
        print("="*50)
        
        # Check if forums already exist
        existing_forums = db.query(Forum).count()
        if existing_forums > 0:
            print(f"⚠️  Found {existing_forums} existing forums. Clearing old data...")
            # Delete in correct order due to foreign keys
            db.query(ResponseLike).delete()
            db.query(PostLike).delete()
            db.query(Response).delete()
            db.query(Post).delete()
            db.query(ForumModerator).delete()
            db.query(Forum).delete()
            db.commit()
        
        # Get or create moderator users for forums
        moderator_users = []
        moderator_emails = [
            "moderator1@sahemind.com",
            "moderator2@sahemind.com",
            "moderator3@sahemind.com"
        ]
        
        for email in moderator_emails:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                user = User(
                    email=email,
                    password_hash=hash_password("moderator123"),
                    role="moderator",
                    is_active=True,
                    created_at=datetime.utcnow(),
                )
                db.add(user)
                print(f"✅ Created moderator: {email}")
            moderator_users.append(user)
        
        db.commit()
        
        # Create forums
        print("\n📋 Creating forums...")
        
        forums_data = [
            {
                "name": "Mental Health Support",
                "description": "A safe space to share your thoughts, feelings, and experiences. Get support and encouragement from our community.",
                "thematic": "Mental Health",
                "moderators": [moderator_users[0]],
            },
            {
                "name": "Anxiety & Stress Management",
                "description": "Discuss strategies, coping mechanisms, and support for managing anxiety and stress in daily life.",
                "thematic": "Anxiety",
                "moderators": [moderator_users[0], moderator_users[1]],
            },
            {
                "name": "Depression Support Group",
                "description": "A supportive community for those dealing with depression. Share your journey and find hope.",
                "thematic": "Depression",
                "moderators": [moderator_users[1]],
            },
            {
                "name": "Wellness & Self-Care",
                "description": "Tips, advice, and discussions about wellness practices, self-care routines, and healthy habits.",
                "thematic": "Wellness",
                "moderators": [moderator_users[2]],
            },
            {
                "name": "Emotional Support & Healing",
                "description": "A place to discuss emotional experiences, healing journeys, and personal growth.",
                "thematic": "Emotional Support",
                "moderators": [moderator_users[2]],
            },
        ]
        
        forums = []
        for forum_data in forums_data:
            forum = Forum(
                name=forum_data["name"],
                description=forum_data["description"],
                thematic=forum_data["thematic"],
                is_active=True,
                created_at=datetime.utcnow(),
            )
            db.add(forum)
            db.flush()  # Flush to get the forum ID
            
            # Add moderators to the forum
            for moderator in forum_data["moderators"]:
                forum_mod = ForumModerator(
                    forum_id=forum.id,
                    user_id=moderator.id,
                    assigned_at=datetime.utcnow(),
                )
                db.add(forum_mod)
            
            forums.append(forum)
            print(f"✅ Created forum: {forum.name}")
        
        db.commit()
        
        # Get users for creating posts (use existing users or create new ones)
        print("\n👥 Getting users for posts...")
        
        user1 = db.query(User).filter(User.role == "patient").first()
        if not user1:
            user1 = User(
                email="patient1@sahamind.com",
                password_hash=hash_password("patient123"),
                role="patient",
                is_active=True,
                created_at=datetime.utcnow(),
            )
            db.add(user1)
            print(f"✅ Created user: patient1@sahamind.com")
        
        # Create a few more users for varied posts
        additional_users = []
        additional_emails = [
            "user2@sahamind.com",
            "user3@sahamind.com",
            "user4@sahamind.com",
            "user5@sahamind.com",
        ]
        
        for email in additional_emails:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                user = User(
                    email=email,
                    password_hash=hash_password("password123"),
                    role="patient",
                    is_active=True,
                    created_at=datetime.utcnow(),
                )
                db.add(user)
                additional_users.append(user)
                print(f"✅ Created user: {email}")
            else:
                additional_users.append(user)
        
        db.commit()
        
        all_users = [user1] + additional_users
        
        # Create posts for each forum
        print("\n📝 Creating posts...")
        
        posts_data = [
            # Mental Health Support Forum
            {
                "forum_idx": 0,
                "title": "Starting my mental health journey",
                "content": "I've decided to finally prioritize my mental health. After years of ignoring my feelings, I'm taking the first step by reaching out and talking about it. I'm nervous but hopeful that this community can help me through this process.",
                "author_idx": 0,
                "is_anonymous": False,
                "days_ago": 10,
            },
            {
                "forum_idx": 0,
                "title": "Small wins matter",
                "content": "Today I accomplished something I didn't think I could do. I went to the park by myself and spent an hour there just breathing and observing nature. It might seem small, but for me it's a huge step. I'm learning that progress isn't always linear, and that's okay.",
                "author_idx": 1,
                "is_anonymous": False,
                "days_ago": 8,
            },
            {
                "forum_idx": 0,
                "title": "Finding strength in community",
                "content": "Thank you all for being here. This community has shown me that I'm not alone in my struggles. Knowing that others understand what I'm going through has made such a difference in my healing journey.",
                "author_idx": 2,
                "is_anonymous": True,
                "days_ago": 6,
            },
            
            # Anxiety & Stress Management Forum
            {
                "forum_idx": 1,
                "title": "My anxiety management routine",
                "content": "I've been practicing deep breathing exercises for 2 weeks now, and they're really helping! I do 5 minutes of box breathing every morning and evening. Combined with journaling, I've noticed my anxiety levels have decreased significantly. Wanted to share in case it helps anyone else.",
                "author_idx": 0,
                "is_anonymous": False,
                "days_ago": 9,
            },
            {
                "forum_idx": 1,
                "title": "Dealing with work stress",
                "content": "Work has been overwhelming lately with tight deadlines and demanding clients. I'm trying to establish boundaries and not work on weekends, but it's been challenging. Has anyone else dealt with similar situations? How did you manage to balance work and mental health?",
                "author_idx": 3,
                "is_anonymous": False,
                "days_ago": 7,
            },
            {
                "forum_idx": 1,
                "title": "Panic attacks at night",
                "content": "I've been experiencing panic attacks mostly in the evenings. They're terrifying and exhausting. I'm learning that they won't harm me, but it's still scary when they happen. Any advice or personal experiences would be appreciated.",
                "author_idx": 4,
                "is_anonymous": True,
                "days_ago": 5,
            },
            
            # Depression Support Group Forum
            {
                "forum_idx": 2,
                "title": "Good days and bad days",
                "content": "Depression is not a straight line. Some days I feel okay, even hopeful. Other days it feels like I'm back to square one. I'm learning to be gentle with myself on the hard days and celebrate the good ones. If you're struggling, know that it gets better.",
                "author_idx": 1,
                "is_anonymous": False,
                "days_ago": 8,
            },
            {
                "forum_idx": 2,
                "title": "Medication and therapy",
                "content": "Started antidepressants 3 months ago and combined with therapy, I'm noticing real improvements. It wasn't easy to ask for help, but I'm so glad I did. For anyone on the fence about medication, I'd say give it a try and work with your doctor to find what works for you.",
                "author_idx": 2,
                "is_anonymous": False,
                "days_ago": 10,
            },
            {
                "forum_idx": 2,
                "title": "Lost motivation",
                "content": "I'm struggling to find motivation for basic tasks. Even things I used to enjoy feel like they require so much energy. Is anyone else experiencing this? What helps you push through?",
                "author_idx": 3,
                "is_anonymous": True,
                "days_ago": 4,
            },
            
            # Wellness & Self-Care Forum
            {
                "forum_idx": 3,
                "title": "Morning meditation changed my life",
                "content": "I started meditating 20 minutes every morning 6 months ago, and it's been transformative. I'm more present, less reactive, and genuinely feel more at peace. I'm using an app that guides me through the meditation. Highly recommend trying it!",
                "author_idx": 4,
                "is_anonymous": False,
                "days_ago": 7,
            },
            {
                "forum_idx": 3,
                "title": "Self-care routine ideas",
                "content": "What does self-care look like for you? I've been experimenting with different activities - journaling, bubble baths, long walks, reading. I find that mixing physical and mental activities works best for me. Would love to hear what works for others!",
                "author_idx": 0,
                "is_anonymous": False,
                "days_ago": 6,
            },
            {
                "forum_idx": 3,
                "title": "Exercise and mental health",
                "content": "Started going to the gym 3 times a week, and the mental health benefits are incredible. Exercise releases endorphins that genuinely improve my mood. Even just 30 minutes of walking makes a difference. If anyone is struggling with motivation to exercise, start small!",
                "author_idx": 1,
                "is_anonymous": False,
                "days_ago": 5,
            },
            
            # Emotional Support & Healing Forum
            {
                "forum_idx": 4,
                "title": "Processing past trauma",
                "content": "I've started working with a trauma-informed therapist, and it's helping me process past experiences. It's difficult work, but I can feel myself healing. To anyone dealing with trauma, know that healing is possible.",
                "author_idx": 2,
                "is_anonymous": False,
                "days_ago": 9,
            },
            {
                "forum_idx": 4,
                "title": "Building healthy relationships",
                "content": "I've been learning about healthy communication and boundaries in relationships. It's changed how I interact with others. Setting boundaries used to make me feel guilty, but I'm learning it's necessary for my wellbeing.",
                "author_idx": 3,
                "is_anonymous": False,
                "days_ago": 6,
            },
            {
                "forum_idx": 4,
                "title": "Self-compassion journey",
                "content": "I used to be very self-critical, but I'm learning to treat myself with the same compassion I'd give to a friend. It's a work in progress, but noticing a real shift in my self-talk and how I handle mistakes.",
                "author_idx": 4,
                "is_anonymous": True,
                "days_ago": 3,
            },
        ]
        
        posts = []
        for post_data in posts_data:
            forum = forums[post_data["forum_idx"]]
            author = all_users[post_data["author_idx"]]
            created_at = datetime.utcnow() - timedelta(days=post_data["days_ago"])
            
            post = Post(
                forum_id=forum.id,
                author_id=author.id,
                title=post_data["title"],
                content=post_data["content"],
                is_anonymous=post_data["is_anonymous"],
                is_reported=False,
                created_at=created_at,
                updated_at=created_at,
            )
            db.add(post)
            posts.append(post)
            print(f"✅ Created post: {post.title}")
        
        db.commit()
        
        # Create responses and likes
        print("\n💬 Creating responses and likes...")
        
        # Add a few responses to some posts
        if len(posts) > 0:
            # Response to first post
            response1 = Response(
                post_id=posts[0].id,
                author_id=all_users[1].id,
                content="Your courage in taking this step is admirable. I'm on a similar journey, and this community has been so helpful. You're not alone in this.",
                is_anonymous=False,
                created_at=datetime.utcnow() - timedelta(days=9),
                updated_at=datetime.utcnow() - timedelta(days=9),
            )
            db.add(response1)
            
            # Response to another post
            response2 = Response(
                post_id=posts[3].id,
                author_id=all_users[2].id,
                content="Thank you for sharing this! I've been wanting to try breathing exercises. I'll definitely give box breathing a try.",
                is_anonymous=False,
                created_at=datetime.utcnow() - timedelta(days=8),
                updated_at=datetime.utcnow() - timedelta(days=8),
            )
            db.add(response2)
            
            # Response to another post
            response3 = Response(
                post_id=posts[6].id,
                author_id=all_users[0].id,
                content="You're describing exactly what I'm experiencing. Please know that with proper support and treatment, things do improve. Hang in there.",
                is_anonymous=False,
                created_at=datetime.utcnow() - timedelta(days=7),
                updated_at=datetime.utcnow() - timedelta(days=7),
            )
            db.add(response3)
            
            db.commit()
            
            # Add likes to posts
            print("💖 Adding likes to posts...")
            
            # Like posts
            for i, post in enumerate(posts[:10]):  # Add likes to first 10 posts
                for j in range(i % 3 + 1):  # Each post gets 1-3 likes
                    post_like = PostLike(
                        post_id=post.id,
                        user_id=all_users[j % len(all_users)].id,
                        created_at=datetime.utcnow() - timedelta(days=max(1, post_data["days_ago"] - 1)),
                    )
                    db.add(post_like)
                    print(f"✅ Added like to post: {post.title}")
            
            db.commit()
        
        print("\n" + "="*50)
        print("✅ Forum seed completed successfully!")
        print(f"📊 Created {len(forums)} forums")
        print(f"📝 Created {len(posts)} posts")
        print("="*50)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_forums_and_posts()
