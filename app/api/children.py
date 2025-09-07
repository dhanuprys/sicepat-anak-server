from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.auth import get_current_user
from app.crud import (
    create_children, get_children_by_id, get_children_by_user,
    update_children, delete_children
)
from app.models import User
from app.schemas import ChildrenCreate, ChildrenUpdate, ChildrenResponse

router = APIRouter(prefix="/children", tags=["children"])


@router.post("/", response_model=ChildrenResponse, status_code=status.HTTP_201_CREATED)
def create_new_children(
    children_data: ChildrenCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new children"""
    children = create_children(db, children_data, current_user.id)
    return children


@router.get("/", response_model=List[ChildrenResponse])
def get_user_children(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all children for current user"""
    children = get_children_by_user(db, current_user.id)
    return children


@router.get("/{children_id}", response_model=ChildrenResponse)
def get_children_detail(
    children_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific children detail"""
    children = get_children_by_id(db, children_id, current_user.id)
    if not children:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Children not found"
        )
    return children


@router.put("/{children_id}", response_model=ChildrenResponse)
def update_children_data(
    children_id: int,
    children_update: ChildrenUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update children data"""
    updated_children = update_children(db, children_id, current_user.id, children_update)
    if not updated_children:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Children not found"
        )
    return updated_children


@router.delete("/{children_id}")
def delete_children_data(
    children_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete children data"""
    success = delete_children(db, children_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Children not found"
        )
    return {"message": "Children deleted successfully"}
