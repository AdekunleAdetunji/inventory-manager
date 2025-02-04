#!/usr/bin/env python3
"""
This module contains the base orm model class definition of the inventory application
pydantic models
"""
from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict
from uuid import UUID

# base configuration for all models
base_config = ConfigDict(from_attributes=True)


class Base:
    """Baseclass from which all response model validators inherit"""

    id: UUID
    created: datetime
    updated: datetime


class BaseResponseValidator(Base, BaseModel):
    """
    Validator class for validating child model objects linked to a parent model
    object
    """

    model_config = base_config
