#!/usr/bin/env python3
"""
This module contains the definition of the SQLAlchemy inventory model
"""
from main.database.models.basemodel import BaseModel
from main.database.models.inven_transaction import InventoryTransaction
from sqlalchemy import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Inventory(BaseModel):
    """Model to hold record of all product inventories"""

    __tablename__ = "inventory"

    country: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    product_id: Mapped[UUID] = mapped_column(ForeignKey("product.id"))
    product: Mapped["Product"] = relationship(back_populates="inventories")  # type: ignore
    transactions: Mapped[list["InventoryTransaction"]] = relationship(
        back_populates="inventory",
    )
