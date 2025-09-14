#!/usr/bin/env python3
"""
Script untuk set user menjadi admin
"""

import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User

def set_user_admin(username: str, is_admin: bool = True):
    """Set user admin status"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            print(f"❌ User '{username}' not found")
            return False
        
        user.is_admin = is_admin
        db.commit()
        db.refresh(user)
        
        print(f"✅ User '{username}' admin status set to: {is_admin}")
        print(f"   User ID: {user.id}")
        print(f"   Username: {user.username}")
        print(f"   Is Admin: {user.is_admin}")
        return True
        
    except Exception as e:
        print(f"❌ Error setting admin status: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def list_users():
    """List all users"""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print("📋 All Users:")
        for user in users:
            print(f"   ID: {user.id}, Username: {user.username}, Is Admin: {user.is_admin}")
    except Exception as e:
        print(f"❌ Error listing users: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python set_admin.py list                    # List all users")
        print("  python set_admin.py <username>              # Set user as admin")
        print("  python set_admin.py <username> false        # Remove admin status")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "list":
        list_users()
    else:
        username = command
        is_admin = True
        if len(sys.argv) > 2 and sys.argv[2].lower() == "false":
            is_admin = False
        
        set_user_admin(username, is_admin)
