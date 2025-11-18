import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from urllib.parse import quote_plus

# Import all models, including the new User model
from models import Base, Topic, User

# Load environment variables from .env
# ============================================================================
# Load Environment Variables
# ============================================================================
load_dotenv()
# SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")

# Fetch variables
DB_USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")
if not DB_USER or not PASSWORD or not HOST or not PORT or not DBNAME:
    print("❌ ERROR: one or more DB variables are not in .env file")
    exit(1)
# if password contain special character
encoded_password = quote_plus(PASSWORD)
# Construct the SQLAlchemy connection string
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{encoded_password}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
# print(f"DATABASE_URL: {DATABASE_URL}")
# Create the SQLAlchemy engine
# engine = create_engine(DATABASE_URL)
# If using Transaction Pooler or Session Pooler, we want to ensure we disable SQLAlchemy client side pooling -
# https://docs.sqlalchemy.org/en/20/core/pooling.html#switching-pool-implementations
engine = create_engine(DATABASE_URL, poolclass=NullPool)
SessionLocal = sessionmaker(bind=engine)
# Test the connection
# try:
#     with engine.connect() as connection:
#         print("Connection successful!")
# except Exception as e:
#     print(f"Failed to connect: {e}")

# ============================================================================
# Database Setup
# ============================================================================
# engine = create_engine(SUPABASE_DB_URL)
# SessionLocal = sessionmaker(bind=engine)

# ============================================================================
# Create Tables
# ============================================================================
if __name__ == "__main__":
    # This will now create the 'users' table and add the 'user_id'
    # column to the 'reflections' table automatically.
    Base.metadata.create_all(bind=engine)
    
    # Insert initial topics
    db = SessionLocal()
    try:
        initial_topics = ["learning", "surfing", "parenting", "arts", "productivity", "relationships", "health"]
        for topic_name in initial_topics:
            if not db.query(Topic).filter(Topic.name == topic_name).first():
                db.add(Topic(name=topic_name))
        users = [
            {"firstname": "John", "email": "john@test.com"}, 
            {"firstname": "Jane", "email": "jane@test.com"},
            {"firstname": "Alice", "email": "alice@test.com"}
        ]
        for u in users:
            if not db.query(User).filter(User.firstname == u["firstname"]).first():
                db.add(User(firstname=u["firstname"], email=u["email"]))
        db.commit()
        print("✅ Tables created and topics and users seeded successfully!")
    finally:
        db.close()