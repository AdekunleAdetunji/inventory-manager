#!/usr/bin/env python3
"""
This module contains the definition of the product orm model
"""
from main.database.models.basemodel import BaseModel
from main.database.models.inventory import Inventory
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Product(BaseModel):
    """inventory product model"""

    __tablename__ = "product"

    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    sku: Mapped[str] = mapped_column(String(8), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[float] = mapped_column(nullable=False)
    category_id: Mapped[UUID] = mapped_column(ForeignKey("category.id"))
    is_active: Mapped[bool] = mapped_column(default=True)
    category: Mapped["Category"] = relationship(back_populates="products")  # type: ignore
    inventories: Mapped[list["Inventory"]] = relationship(
        back_populates="product"
    )
