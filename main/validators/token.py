#!/usr/bin/python3
"""
This module contains the validator for authentication token
"""
from pydantic import BaseModel
from pydantic import EmailStr


class Token(BaseModel):
    """Authentication token validator model"""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Authentication token data"""

    email: EmailStr
