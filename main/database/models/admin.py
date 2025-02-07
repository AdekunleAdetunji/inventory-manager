#!/usr/bin/python3
"""
This module contains the sqlalchemy admin model to store administrator
credentials
"""
from main.database.models.basemodel import BaseModel
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy_utils import EmailType
from sqlalchemy_utils import PasswordType

# from sqlalchemy_utils import Password


class Admin(BaseModel):
    """inventory database administrator model"""

    __tablename__ = "admin"

    email: Mapped[str] = mapped_column(EmailType, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(
        PasswordType(schemes=["pbkdf2_sha512"]), nullable=False
    )
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
