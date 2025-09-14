from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
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


class ChildrenBase(BaseModel):
    name: str
    gender: str
    dob: date
    
    @validator('gender')
    def validate_gender(cls, v):
        if v not in ['L', 'P']:
            raise ValueError('Gender must be L or P')
        return v


class DiagnoseHistoryBase(BaseModel):
    age_on_month: int
    gender: str
    height: int
    result: str
    
    @validator('age_on_month')
    def validate_age(cls, v):
        if v < 0 or v > 60:
            raise ValueError('Age must be between 0 and 60 months')
        return v
    
    @validator('height')
    def validate_height(cls, v):
        if v < 30 or v > 200:
            raise ValueError('Height must be between 30 and 200 cm')
        return v
    
    @validator('result')
    def validate_result(cls, v):
        valid_results = ['Normal', 'Severely Stunted', 'Stunted', 'Tinggi']
        if v not in valid_results:
            raise ValueError('Result must be one of: Normal, Severely Stunted, Stunted, Tinggi')
        return v


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


class ChildrenCreate(ChildrenBase):
    user_id: Optional[int] = None  # Optional for regular users, required for admin
    
    @validator('name')
    def trim_name(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class DiagnoseHistoryCreate(BaseModel):
    age_on_month: int
    gender: str
    height: int
    
    @validator('age_on_month')
    def validate_age(cls, v):
        if v < 0 or v > 60:
            raise ValueError('Age must be between 0 and 60 months')
        return v
    
    @validator('height')
    def validate_height(cls, v):
        if v < 30 or v > 200:
            raise ValueError('Height must be between 30 and 200 cm')
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


class ChildrenUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[date] = None
    
    @validator('name')
    def trim_name(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


# Response schemas
class UserResponse(UserBase):
    id: int
    registration_date: datetime
    
    class Config:
        from_attributes = True


class ChildrenResponse(ChildrenBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DiagnoseHistoryResponse(DiagnoseHistoryBase):
    id: int
    children_id: int
    diagnosed_at: datetime
    
    class Config:
        from_attributes = True


class DiagnoseResult(BaseModel):
    result: str


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
