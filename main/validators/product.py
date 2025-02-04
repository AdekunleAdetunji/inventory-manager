#!/usr/bin/env python3
"""
This module contains the pydantic model for validation of input and output data
for the product orm model
"""
from main.validators.basemodel import Base
from main.validators.basemodel import base_config
from main.validators.basemodel import BaseResponseValidator
from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class ProductRequestValidator(BaseModel):
    """Validator model for product model data recieved from a web request"""

    model_config = base_config

    name: str
    sku: str
    description: Optional[str] = None
    price: float
    category_id: UUID
    is_active: bool = True


class ProductResponseValidator(Base, ProductRequestValidator):
    """Validator model for product data sent with a web response"""

    inventories: list[BaseResponseValidator]
