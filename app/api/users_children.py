"""
API endpoints untuk children management (Admin only)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, Children
from app.schemas import ChildrenResponse, ChildrenCreate, ChildrenUpdate
from app.middleware import get_admin_user
from app.crud import (
    get_children_by_id_admin, 
    get_all_children, 
    get_children_by_user_id,
    create_children_admin, 
    update_children_admin, 
    delete_children_admin
)

router = APIRouter()

@router.get("/", response_model=List[ChildrenResponse])
def get_all_children_endpoint(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get all children from all users (Admin only)"""
    children = get_all_children(db)
    return children

@router.get("/{children_id}", response_model=ChildrenResponse)
def get_children_by_id_endpoint(
    children_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get children by ID (Admin only)"""
    children = get_children_by_id_admin(db, children_id)
    if not children:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Children not found"
        )
    return children

@router.get("/user/{user_id}", response_model=List[ChildrenResponse])
def get_children_by_user_id_endpoint(
    user_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get all children by user ID (Admin only)"""
    children = get_children_by_user_id(db, user_id)
    return children

@router.post("/", response_model=ChildrenResponse)
def create_children_endpoint(
    children_data: ChildrenCreate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Create children for any user (Admin only)"""
    children = create_children_admin(db, children_data)
    return children

@router.put("/{children_id}", response_model=ChildrenResponse)
def update_children_endpoint(
    children_id: int,
    children_update: ChildrenUpdate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Update children by ID (Admin only)"""
    children = get_children_by_id_admin(db, children_id)
    if not children:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Children not found"
        )
    
    updated_children = update_children_admin(db, children_id, children_update)
    return updated_children

@router.delete("/{children_id}")
def delete_children_endpoint(
    children_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Delete children by ID (Admin only)"""
    children = get_children_by_id_admin(db, children_id)
    if not children:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Children not found"
        )
    
    delete_children_admin(db, children_id)
    return {"message": "Children deleted successfully"}
