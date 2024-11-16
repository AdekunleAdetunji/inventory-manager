#!/usr/bin/env python3
"""
This module contains the pydantic model for validation of input and output data
for the category orm model
"""
from main.validators.basemodel import Base
from main.validators.basemodel import base_config
from pydantic import BaseModel
from typing import Optional


class CategoryRequestValidator(BaseModel):
    """
    Model to handle validation of request body for operations on the category
    ORM model
    """

    model_config = base_config

    name: str
    code: str
    description: str
    products: Optional[list] = None


class CategoryResponseValidator(Base, CategoryRequestValidator):
    """
    Model to handle validation of data that is being retrieved from the
    inventory database category table
    """

    pass
