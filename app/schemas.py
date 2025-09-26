from pydantic import BaseModel, validator
from typing import Optional
from datetime import date, datetime


# Base schemas
class UserBase(BaseModel):
    avatar_type: int
    name: str
    username: str
    address: Optional[str] = None
    dob: date
    gender: str
    is_admin: Optional[bool] = False


# Create schemas
class UserCreate(UserBase):
    password: str
    
    @validator('username', 'name', 'address', 'password')
    def trim_strings(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        return v


# Update schemas
class UserUpdate(BaseModel):
    avatar_type: Optional[int] = None
    name: Optional[str] = None
    username: Optional[str] = None
    address: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    is_admin: Optional[bool] = None
    
    @validator('name', 'username', 'address')
    def trim_strings(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


# Response schemas
class UserResponse(UserBase):
    id: int
    registration_date: datetime
    
    class Config:
        from_attributes = True


# Auth schemas
class UserLogin(BaseModel):
    username: str
    password: str
    
    @validator('username', 'password')
    def trim_strings(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class UserRegister(UserCreate):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class TokenData(BaseModel):
    username: Optional[str] = None


class PasswordChange(BaseModel):
    new_password: str
    
    @validator('new_password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        return v
