"""
REST API for Reflection Management
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from urllib.parse import quote_plus

# Import all models, including the new User model
from .models import Base, Topic, Reflection, User
from .classifier import classify_reflection_topics

# ============================================================================
# Load Environment Variables
# ============================================================================
load_dotenv()

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")
if not USER or not PASSWORD or not HOST or not PORT or not DBNAME:
    print("❌ ERROR: one or more DB variables are not in .env file")
    exit(1)
# if password contain special character
encoded_password = quote_plus(PASSWORD)
# Construct the SQLAlchemy connection string
DATABASE_URL = f"postgresql+psycopg2://{USER}:{encoded_password}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# If using Transaction Pooler or Session Pooler, we want to ensure we disable SQLAlchemy client side pooling -
# https://docs.sqlalchemy.org/en/20/core/pooling.html#switching-pool-implementations
engine = create_engine(DATABASE_URL, poolclass=NullPool)
SessionLocal = sessionmaker(bind=engine)

# ============================================================================
# FastAPI App
# ============================================================================
app = FastAPI(title="Reflection API")

# ============================================================================
# Pydantic Models
# ============================================================================
class ClassifyReflectionInput(BaseModel):
    title: str
    text: str
    timestamp: datetime

class ClassifyReflectionOutput(BaseModel):
    topics: List[str]

class CreateReflectionInput(BaseModel):
    title: str
    text: str
    timestamp: datetime
    topics: List[str]
    user_id: int  # <-- NECESSARY CHANGE: Added user_id

class CreateReflectionOutput(BaseModel):
    reflection_id: int

class TopicsInput(BaseModel):
    names: List[str]

class TopicOutput(BaseModel):
    id: int
    name: str

# ============================================================================
# NEW: Pydantic Models for User
# ============================================================================
class UserCreateInput(BaseModel):
    firstname: str | None = None
    email: str

class UserOutput(BaseModel):
    id: int
    firstname: str | None
    email: str

# ============================================================================
# Database Helper Functions without API Endpoints and async for frontend use 
# ============================================================================

def db_get_all_users():
    """Get all users - can be called directly from frontend"""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        return [UserOutput(id=u.id, firstname=u.firstname, email=u.email) for u in users]
    finally:
        db.close()

def db_get_user(user_id: int):
    """Get a user by ID - can be called directly from frontend"""
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserOutput(id=db_user.id, firstname=db_user.firstname, email=db_user.email)
    finally:
        db.close()

def db_get_all_reflections():
    """Get all reflections - can be called directly from frontend"""
    db = SessionLocal()
    try:
        reflections = db.query(Reflection).all()
        return [
            {
                "id": r.id,
                "title": r.title,
                "text": r.text,
                "timestamp": r.timestamp,
                "user_id": r.user_id,
                "topics": [t.name for t in r.topic_list]
            }
            for r in reflections
        ]
    finally:
        db.close()

def db_get_reflection(reflection_id: int):
    """Get a single reflection - can be called directly from frontend"""
    db = SessionLocal()
    try:
        db_reflection = db.query(Reflection).filter(Reflection.id == reflection_id).first()
        
        if not db_reflection:
            raise HTTPException(status_code=404, detail="Reflection not found")
            
        return {
            "id": db_reflection.id,
            "title": db_reflection.title,
            "text": db_reflection.text,
            "timestamp": db_reflection.timestamp,
            "user_id": db_reflection.user_id,
            "topics": [t.name for t in db_reflection.topic_list]
        }
    finally:
        db.close()

async def db_classify_reflection(reflection: ClassifyReflectionInput):
    """Classify a reflection - can be called directly from frontend"""
    db = SessionLocal()
    try:
        all_topics = db.query(Topic).all()
        existing_topic_names = [t.name for t in all_topics]
        
        topics = await classify_reflection_topics(
            reflection.title,
            reflection.text,
            existing_topic_names
        )
        
        return ClassifyReflectionOutput(topics=topics)
    finally:
        db.close()

async def db_create_reflection(reflection: CreateReflectionInput):
    """Create a reflection - can be called directly from frontend"""
    db = SessionLocal()
    try:
        # Check if user exists first
        user = db.query(User).filter(User.id == reflection.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"User with id {reflection.user_id} not found")

        # Create the reflection
        db_reflection = Reflection(
            title=reflection.title,
            text=reflection.text,
            timestamp=reflection.timestamp,
            user_id=reflection.user_id
        )
        
        # Add the reflection to the session FIRST
        db.add(db_reflection)
        
        # Then add topics
        for topic_name in reflection.topics:
            topic = db.query(Topic).filter(Topic.name == topic_name).first()
            if not topic:
                topic = Topic(name=topic_name)
                db.add(topic)
                db.flush()  # Flush to ensure topic gets an ID
            db_reflection.topic_list.append(topic)
        
        db.commit()
        db.refresh(db_reflection)
        
        return CreateReflectionOutput(reflection_id=db_reflection.id)
    finally:
        db.close()

# ============================================================================
# API Endpoints for run api server - modified create_reflection
# ============================================================================
@app.get("/")
async def root():
    """Check if the API is running"""
    return {"status": "ok"}

# --- Topic Endpoints (Unchanged) ---

@app.post("/api/topics", response_model=List[TopicOutput])
async def create_topics(topics: TopicsInput):
    """Add new topics to the database"""
    db = SessionLocal()
    try:
        created_topics = []
        for name in topics.names:
            existing = db.query(Topic).filter(Topic.name == name).first()
            if not existing:
                db_topic = Topic(name=name)
                db.add(db_topic)
                # Flush to get ID before commit
                db.flush()
                created_topics.append(db_topic)
            else:
                created_topics.append(existing)
        db.commit()
        return [TopicOutput(id=t.id, name=t.name) for t in created_topics]
    finally:
        db.close()

@app.get("/api/topics", response_model=List[TopicOutput])
async def get_topics():
    """Retrieve all topics from the database"""
    db = SessionLocal()
    try:
        topics = db.query(Topic).all()
        return [TopicOutput(id=t.id, name=t.name) for t in topics]
    finally:
        db.close()

# --- Reflection Endpoints (create_reflection is modified) ---

@app.post("/api/reflections", response_model=CreateReflectionOutput)
async def create_reflection(reflection: CreateReflectionInput):
    """Store a new reflection in the database"""
    db = SessionLocal()
    try:
        # Check if user exists first (good practice)
        user = db.query(User).filter(User.id == reflection.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"User with id {reflection.user_id} not found")

        # Create the reflection with the new user_id field
        db_reflection = Reflection(
            title=reflection.title,
            text=reflection.text,
            timestamp=reflection.timestamp,
            user_id=reflection.user_id  # <-- NECESSARY CHANGE
        )
        
        # Topic logic is unchanged
        for topic_name in reflection.topics:
            topic = db.query(Topic).filter(Topic.name == topic_name).first()
            if not topic:
                topic = Topic(name=topic_name)
                db.add(topic)
            db_reflection.topic_list.append(topic)
        
        db.add(db_reflection)
        db.commit()
        db.refresh(db_reflection)
        
        return CreateReflectionOutput(reflection_id=db_reflection.id)
    finally:
        db.close()

@app.get("/api/reflections/{reflection_id}")
async def get_reflection(reflection_id: int):
    """Retrieve a single reflection by its ID"""
    db = SessionLocal()
    try:
        db_reflection = db.query(Reflection).filter(Reflection.id == reflection_id).first()
        
        if not db_reflection:
            raise HTTPException(status_code=404, detail="Reflection not found")
            
        return {
            "id": db_reflection.id, # Added id
            "title": db_reflection.title,
            "text": db_reflection.text,
            "timestamp": db_reflection.timestamp,
            "user_id": db_reflection.user_id, # Added user_id
            "topics": [t.name for t in db_reflection.topic_list]
        }
    finally:
        db.close()

@app.get("/api/reflections")
async def get_all_reflections():
    """Retrieve all reflections"""
    db = SessionLocal()
    try:
        reflections = db.query(Reflection).all()
        return [
            {
                "id": r.id,
                "title": r.title,
                "text": r.text,
                "timestamp": r.timestamp,
                "user_id": r.user_id, # Added user_id
                "topics": [t.name for t in r.topic_list]
            }
            for r in reflections
        ]
    finally:
        db.close()        

@app.post("/api/reflections/classify", response_model=ClassifyReflectionOutput)
async def classify_reflection(reflection: ClassifyReflectionInput):
    """Classify topics from a reflection"""
    db = SessionLocal()
    try:
        all_topics = db.query(Topic).all()
        existing_topic_names = [t.name for t in all_topics]
        
        topics = await classify_reflection_topics(
            reflection.title,
            reflection.text,
            existing_topic_names
        )
        
        return ClassifyReflectionOutput(topics=topics)
    finally:
        db.close()

# ============================================================================
# NEW: User Endpoints for curl commands
# ============================================================================

@app.post("/api/users", response_model=UserOutput)
async def create_user(user: UserCreateInput):
    """Create a new user"""
    db = SessionLocal()
    try:
        # Check if email already exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
            
        db_user = User(
            firstname=user.firstname,
            email=user.email
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return UserOutput(id=db_user.id, firstname=db_user.firstname, email=db_user.email)
    finally:
        db.close()

@app.get("/api/users/{user_id}", response_model=UserOutput)
async def get_user(user_id: int):
    """Get a user by their ID"""
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserOutput(id=db_user.id, firstname=db_user.firstname, email=db_user.email)
    finally:
        db.close()

@app.get("/api/users", response_model=List[UserOutput])
async def get_all_users():
    """Get all users"""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        return [
            UserOutput(id=u.id, firstname=u.firstname, email=u.email)
            for u in users
        ]
    finally:
        db.close()

# ============================================================================
# Run the application
# ============================================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="localhost", port=8000, reload=True)

