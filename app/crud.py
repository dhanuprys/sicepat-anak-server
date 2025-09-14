from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional, Union
from app.models import User, Children, DiagnoseHistory
from app.schemas import UserCreate, UserUpdate, ChildrenCreate, ChildrenUpdate, DiagnoseHistoryCreate
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


# Children CRUD operations
def create_children(db: Session, children: ChildrenCreate, user_id: int) -> Children:
    """Create new children"""
    db_children = Children(
        user_id=user_id,
        name=children.name,
        gender=children.gender,
        dob=children.dob
    )
    db.add(db_children)
    db.commit()
    db.refresh(db_children)
    return db_children


def get_children_by_id(db: Session, children_id: int, user_id: int) -> Optional[Children]:
    """Get children by ID (belonging to specific user)"""
    return db.query(Children).filter(
        and_(Children.id == children_id, Children.user_id == user_id)
    ).first()


def get_children_by_user(db: Session, user_id: int) -> List[Children]:
    """Get all children for a specific user"""
    return db.query(Children).filter(Children.user_id == user_id).all()


def get_all_children(db: Session) -> List[Children]:
    """Get all children from all users (Admin only)"""
    return db.query(Children).all()


def get_children_by_id_admin(db: Session, children_id: int) -> Optional[Children]:
    """Get children by ID (Admin only - no user restriction)"""
    return db.query(Children).filter(Children.id == children_id).first()


def get_children_by_user_id(db: Session, user_id: int) -> List[Children]:
    """Get all children by user ID (Admin only)"""
    return db.query(Children).filter(Children.user_id == user_id).all()


def create_children_admin(db: Session, children: ChildrenCreate) -> Children:
    """Create children for any user (Admin only)"""
    db_children = Children(
        user_id=children.user_id,
        name=children.name,
        gender=children.gender,
        dob=children.dob
    )
    db.add(db_children)
    db.commit()
    db.refresh(db_children)
    return db_children


def update_children_admin(db: Session, children_id: int, children_update: ChildrenUpdate) -> Optional[Children]:
    """Update children (Admin only - no user restriction)"""
    db_children = get_children_by_id_admin(db, children_id)
    if not db_children:
        return None
    
    update_data = children_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_children, field, value)
    
    db.commit()
    db.refresh(db_children)
    return db_children


def delete_children_admin(db: Session, children_id: int) -> bool:
    """Delete children (Admin only - no user restriction)"""
    db_children = get_children_by_id_admin(db, children_id)
    if not db_children:
        return False
    
    db.delete(db_children)
    db.commit()
    return True


def update_children(db: Session, children_id: int, user_id: int, children_update: ChildrenUpdate) -> Optional[Children]:
    """Update children"""
    db_children = get_children_by_id(db, children_id, user_id)
    if not db_children:
        return None
    
    update_data = children_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_children, field, value)
    
    db.commit()
    db.refresh(db_children)
    return db_children


def delete_children(db: Session, children_id: int, user_id: int) -> bool:
    """Delete children"""
    db_children = get_children_by_id(db, children_id, user_id)
    if not db_children:
        return False
    
    db.delete(db_children)
    db.commit()
    return True


# Diagnose History CRUD operations
def create_diagnose_history(db: Session, diagnose: Union[DiagnoseHistoryCreate, dict], children_id: int) -> DiagnoseHistory:
    """Create new diagnose history"""
    if isinstance(diagnose, dict):
        db_diagnose = DiagnoseHistory(
            children_id=children_id,
            age_on_month=diagnose['age_on_month'],
            gender=diagnose['gender'],
            height=diagnose['height'],
            result=diagnose['result']
        )
    else:
        db_diagnose = DiagnoseHistory(
            children_id=children_id,
            age_on_month=diagnose.age_on_month,
            gender=diagnose.gender,
            height=diagnose.height,
            result=diagnose.result
        )
    
    db.add(db_diagnose)
    db.commit()
    db.refresh(db_diagnose)
    return db_diagnose


def get_diagnose_history_by_id(db: Session, diagnose_id: int, children_id: int) -> Optional[DiagnoseHistory]:
    """Get diagnose history by ID"""
    return db.query(DiagnoseHistory).filter(
        and_(DiagnoseHistory.id == diagnose_id, DiagnoseHistory.children_id == children_id)
    ).first()


def get_diagnose_histories_by_children(db: Session, children_id: int) -> List[DiagnoseHistory]:
    """Get all diagnose histories for a specific children"""
    return db.query(DiagnoseHistory).filter(DiagnoseHistory.children_id == children_id).order_by(DiagnoseHistory.diagnosed_at.desc()).all()


def get_all_diagnose_histories(db: Session) -> List[DiagnoseHistory]:
    """Get all diagnose histories from all users (Admin only)"""
    return db.query(DiagnoseHistory).order_by(DiagnoseHistory.diagnosed_at.desc()).all()


def get_diagnose_by_id_admin(db: Session, diagnose_id: int) -> Optional[DiagnoseHistory]:
    """Get diagnose by ID (Admin only - no user restriction)"""
    return db.query(DiagnoseHistory).filter(DiagnoseHistory.id == diagnose_id).first()


def get_diagnose_histories_by_children_id(db: Session, children_id: int) -> List[DiagnoseHistory]:
    """Get all diagnose histories by children ID (Admin only)"""
    return db.query(DiagnoseHistory).filter(DiagnoseHistory.children_id == children_id).order_by(DiagnoseHistory.diagnosed_at.desc()).all()


def delete_diagnose_history_admin(db: Session, diagnose_id: int) -> bool:
    """Delete diagnose history (Admin only - no user restriction)"""
    db_diagnose = get_diagnose_by_id_admin(db, diagnose_id)
    if not db_diagnose:
        return False
    
    db.delete(db_diagnose)
    db.commit()
    return True
