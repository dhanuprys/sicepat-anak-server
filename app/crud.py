from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import User
from app.schemas import UserCreate, UserUpdate
from app.auth import get_password_hash


# User CRUD operations
def create_user(db: Session, user: UserCreate) -> User:
    """Create new user"""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        avatar_type=user.avatar_type,
        name=user.name,
        username=user.username,
        address=user.address,
        dob=user.dob,
        gender=user.gender,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get user by username"""
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()


def get_all_users(db: Session) -> List[User]:
    """Get all users (Admin only)"""
    return db.query(User).all()


def delete_user(db: Session, user_id: int) -> bool:
    """Delete user (Admin only)"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """Update user"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_password(db: Session, user_id: int, new_password: str) -> Optional[User]:
    """Update user password"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    db_user.password = get_password_hash(new_password)
    db.commit()
    db.refresh(db_user)
    return db_user
