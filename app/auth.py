from datetime import datetime, timedelta
from typing import Optional
import hashlib
import bcrypt
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models import User
from app.schemas import TokenData

# JWT token scheme - using custom header instead of Bearer

# Bcrypt configuration
BCRYPT_ROUNDS = 12


def _pre_hash_password(password: str) -> bytes:
    """
    Pre-hash password with SHA256 to handle passwords longer than 72 bytes.
    Returns raw SHA256 digest (32 bytes) which is well under bcrypt's 72-byte limit.
    This ensures bcrypt never receives input longer than 72 bytes.
    """
    # Encode password to bytes
    password_bytes = password.encode('utf-8')
    # Hash with SHA256 to get fixed 32-byte output
    return hashlib.sha256(password_bytes).digest()


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt with SHA256 pre-hashing.
    This handles passwords of any length safely.
    """
    # Pre-hash with SHA256 to ensure input is always 32 bytes (under 72-byte limit)
    pre_hashed = _pre_hash_password(password)
    # Generate bcrypt hash
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(pre_hashed, salt)
    # Return as string (bcrypt hash is ASCII-safe)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    Uses SHA256 pre-hashing to match the hashing process.
    
    Note: This implementation uses direct bcrypt (not passlib) to avoid
    initialization issues. Existing passwords hashed with passlib will need
    to be reset.
    """
    if not plain_password or not hashed_password:
        return False
    
    try:
        # Pre-hash the plain password
        pre_hashed = _pre_hash_password(plain_password)
        # Verify against stored hash
        return bcrypt.checkpw(pre_hashed, hashed_password.encode('utf-8'))
    except (ValueError, TypeError, AttributeError):
        # Handle invalid hash format or other errors
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """Verify JWT token and return token data"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(
    token: str = Header(..., alias="token"),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from token header"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token header is required",
        )
    
    token_data = verify_token(token)
    
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    return user


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Authenticate user with username and password"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user
