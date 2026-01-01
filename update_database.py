# update_database.py
from core.database import Base, engine

# Import both models
from models.user import User
from models.journal import Journal

print("Dropping all tables...")
Base.metadata.drop_all(bind=engine)

print("Creating all tables with new schema...")
Base.metadata.create_all(bind=engine)

print("✅ Database updated successfully!")
