from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    avatar_type = Column(Integer, nullable=False, default=1)
    name = Column(String(255), nullable=False)
    username = Column(String(100), unique=True, nullable=False, index=True)
    address = Column(Text, nullable=True)
    dob = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, nullable=True, default=False)
    registration_date = Column(DateTime, default=func.now())
    
    # Relationships
    children = relationship("Children", back_populates="user", cascade="all, delete-orphan")
