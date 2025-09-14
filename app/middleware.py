"""
Admin middleware untuk proteksi endpoint admin-only
"""

from fastapi import HTTPException, status, Depends
from app.auth import get_current_user
from app.models import User

def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency untuk memastikan user adalah admin
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin privileges required."
        )
    return current_user
