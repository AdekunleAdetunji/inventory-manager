#!/usr/bin/env python3
"""
This module contains the base orm model class definition of the inventory application
pydantic models
"""
from datetime import datetime
from pydantic import ConfigDict
from uuid import UUID

# base configuration for all models
base_config = ConfigDict(from_attributes=True)


class Base:
    """Baseclass from which all response model object inherits"""

    id: UUID
    created: datetime
    updated: datetime
