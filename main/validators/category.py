#!/usr/bin/env python3
"""
This module contains the pydantic model for validation of input and output data
for the category orm model
"""
from main.validators.basemodel import Base
from main.validators.basemodel import base_config
from main.validators.basemodel import BaseResponseValidator
from pydantic import BaseModel


class CategoryRequestValidator(BaseModel):
    """
    Validator model for category model data recieved from a web request
    """

    model_config = base_config

    name: str
    code: str
    description: str


class CategoryResponseValidator(Base, CategoryRequestValidator):
    """Validator model for category model data sent with a web response"""

    products: list[BaseResponseValidator]
