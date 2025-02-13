#!/usr/bin/python3
"""
This module contains a pydantic validator class to validate data to be sent in
and out of the sqlalchemy admin ORM
"""
from main.validators.basemodel import Base
from main.validators.basemodel import base_config
from pydantic import BaseModel
from pydantic import EmailStr


class PutAdminRequestValidator(BaseModel):
    """
    Validator class for data used in updating an existing sqlalchemy admin ORM
    """

    first_name: str | None = None
    last_name: str | None = None


class NewAdminPassRequestValidator(BaseModel):
    """
    Validator class for new password data sent to the admin sqlalchemy ORM
    """

    old_password: str
    new_password: str


class AdminRequestValidator(BaseModel):
    """Validator class for data going into the sqlalchemy admin ORM"""

    model_config = base_config

    email: EmailStr
    password: str
    first_name: str
    last_name: str


class AdminResponseValidator(Base, BaseModel):
    """Validator class for data sent from the sqlalchemy admin ORM"""

    model_config = base_config

    email: EmailStr
    first_name: str
    last_name: str
