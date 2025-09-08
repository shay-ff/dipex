from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    """Base user schema with common fields"""
    email: EmailStr = Field(..., description="User's email address")
    phone: str = Field(..., description="User's phone number")
    name: Optional[str] = Field(None, description="User's full name")


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=8, description="User's password (minimum 8 characters)")


class UserUpdate(BaseModel):
    """Schema for updating user information"""
    email: Optional[EmailStr] = Field(None, description="User's email address")
    name: Optional[str] = Field(None, description="User's full name")
    password: Optional[str] = Field(None, min_length=8, description="New password (minimum 8 characters)")


class UserInDB(UserBase):
    """Schema for user data in database (includes internal fields)"""
    id: int = Field(..., description="User's unique identifier")
    password_hash: str = Field(..., description="Hashed password")
    created_at: datetime = Field(..., description="Account creation timestamp")
    
    model_config = ConfigDict(from_attributes=True)


class User(UserBase):
    """Schema for user response (excludes sensitive data)"""
    id: int = Field(..., description="User's unique identifier")
    created_at: datetime = Field(..., description="Account creation timestamp")
    
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr = Field(..., description="User's email address")
    phone: Optional[str] = None
    password: str = Field(..., description="User's password")


class Token(BaseModel):
    """Schema for authentication token response"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


class TokenData(BaseModel):
    """Schema for token payload data"""
    email: Optional[str] = None
    phone: Optional[str] = None

class PasswordReset(BaseModel):
    """Schema for password reset request"""
    email: EmailStr = Field(..., description="User's email address")
    phone: str = Field(..., description="User's phone number")

class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation"""
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, description="New password (minimum 8 characters)")


class ChangePassword(BaseModel):
    """Schema for changing password (authenticated user)"""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password (minimum 8 characters)")
