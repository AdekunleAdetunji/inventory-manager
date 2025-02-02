#!/usr/bin/env python3
"""
This module contains the pydantic model for validation of input and output data
for the product orm model
"""
from main.validators.basemodel import Base
from main.validators.basemodel import base_config
from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class ProductRequestValidator(BaseModel):
    """
    Model to handle validation of request body for operations on the product
    ORM model
    """

    model_config = base_config

    name: str
    sku: str
    description: Optional[str] = None
    price: float
    category_id: UUID
    is_active: bool = True


class ProductResponseValidator(Base, ProductRequestValidator):
    """
    Model to handle validation of resonse body for operation on the product
    SQLAlchemy ORM model
    """

    pass
