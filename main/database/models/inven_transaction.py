#!/usr/bin/env python3
"""
This module contains the class definition of inventory transaction orm model
"""
from sqlalchemy import ForeignKey
from sqlalchemy import UUID
from main.database.models.basemodel import BaseModel
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class InventoryTransaction(BaseModel):
    """Model to hold record of each inventory transaction"""

    __tablename__ = "inventory_transaction"

    quantity: Mapped[int] = mapped_column(nullable=False)
    inventory_id: Mapped[UUID] = mapped_column(ForeignKey("inventory.id"))
    inventory: Mapped["Inventory"] = relationship(  # type: ignore
        back_populates="transactions"
    )
