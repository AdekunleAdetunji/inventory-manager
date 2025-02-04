#!/usr/bin/python3
"""
This module contains the validator models for the InventoryTransactions table
"""
from main.validators.basemodel import Base
from main.validators.basemodel import base_config
from pydantic import BaseModel
from uuid import UUID


class InventoryTransactionRequestValidator(BaseModel):
    """
    Validator model for inventory transaction moel data recieved from a web
    request
    """

    model_config = base_config

    quantity: int
    inventory_id: UUID


class InventoryTransactionResponseValidator(
    Base, InventoryTransactionRequestValidator
):
    """
    Validator model for inventory transaction model data sent with a web response
    """

    pass
