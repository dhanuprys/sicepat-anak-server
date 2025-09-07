from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.crud import update_user, update_user_password
from app.models import User
from app.schemas import UserUpdate, UserResponse, PasswordChange

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/", response_model=UserResponse)
def get_current_profile(
    current_user: User = Depends(get_current_user)
):
    """Get current user profile information"""
    return current_user


@router.put("/", response_model=UserResponse)
def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    updated_user = update_user(db, current_user.id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user


@router.put("/change-password")
def change_password(
    password_change: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    updated_user = update_user_password(db, current_user.id, password_change.new_password)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "Password updated successfully"}
