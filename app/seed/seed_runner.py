from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database import Base
from .seed import seed_database
import os
from dotenv import load_dotenv

load_dotenv()

# Use the same DATABASE_URL as the app
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def run_seeding():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Seed the database
    db = SessionLocal()
    try:
        seed_database(db, num_users=10, num_posts=20, num_comments=50)
    finally:
        db.close()

if __name__ == "__main__":
    run_seeding()