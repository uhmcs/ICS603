"""
Database models
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Table, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

reflection_topics = Table(
    'reflection_topics',
    Base.metadata,
    Column('reflection_id', Integer, ForeignKey('reflections.id'), primary_key=True),
    Column('topic_id', Integer, ForeignKey('topics.id'), primary_key=True)
)

# ============================================================================
# NEW USER MODEL
# ============================================================================
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, nullable=True) # Using nullable=True as requested
    email = Column(String, nullable=False, unique=True, index=True)
    
    # This links a User to their Reflections
    reflections = relationship("Reflection", back_populates="user")


class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    reflections = relationship("Reflection", secondary=reflection_topics, back_populates="topic_list")

class Reflection(Base):
    __tablename__ = "reflections"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    
    # ========================================================================
    # ADDED USER ID FOREIGN KEY
    # ========================================================================
    # We make this non-nullable, as a reflection MUST belong to a user.
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # This links a Reflection back to its User
    user = relationship("User", back_populates="reflections")
    
    # This relationship is unchanged
    topic_list = relationship("Topic", secondary=reflection_topics, back_populates="reflections")