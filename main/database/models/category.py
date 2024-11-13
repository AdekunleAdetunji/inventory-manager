#!/usr/bin/env python3
"""
This module contains the category orm model definition for the inventory
databse
"""
from main.database.models.basemodel import BaseModel
from main.database.models.product import Product
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Category(BaseModel):
    """product category inventory model"""

    __tablename__ = "category"

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    code: Mapped[str] = mapped_column(String(5), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
    products: Mapped[list["Product"]] = relationship(
        back_populates="category", cascade="all, delete-orphan"
    )
