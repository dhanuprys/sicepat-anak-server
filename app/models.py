from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Text
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
    registration_date = Column(DateTime, default=func.now())
    
    # Relationships
    children = relationship("Children", back_populates="user", cascade="all, delete-orphan")


class Children(Base):
    __tablename__ = "childrens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    gender = Column(String(10), nullable=False)  # L/P
    dob = Column(Date, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="children")
    diagnose_histories = relationship("DiagnoseHistory", back_populates="children", cascade="all, delete-orphan")


class DiagnoseHistory(Base):
    __tablename__ = "diagnose_histories"
    
    id = Column(Integer, primary_key=True, index=True)
    children_id = Column(Integer, ForeignKey("childrens.id", ondelete="CASCADE"), nullable=False)
    age_on_month = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)  # L/P
    height = Column(Integer, nullable=False)  # Height in cm
    result = Column(String(50), nullable=False)  # Stunting detection result
    diagnosed_at = Column(DateTime, default=func.now())
    
    # Relationships
    children = relationship("Children", back_populates="diagnose_histories")
