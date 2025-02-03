#!/usr/bin/python3
"""
This module contains the pydantic models for validating data going into and out
of the inventory table
"""
from main.validators.basemodel import Base
from main.validators.basemodel import base_config
from main.validators.inventory_transaction import (
    InventoryTransactionResponseValidator,
)
from pydantic import BaseModel
from pydantic_extra_types.country import CountryAlpha2
from uuid import UUID


class InventoryRequestValidator(BaseModel):
    """Validator model for inventory data recieved from a web request"""

    model_config = base_config

    product_id: UUID
    country: CountryAlpha2
    quantity: int


class InventoryResponseValidator(Base, InventoryRequestValidator):
    """Validator model for inventory data web response"""

    transactions: list[InventoryTransactionResponseValidator]
    pass
