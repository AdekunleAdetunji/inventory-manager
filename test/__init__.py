#!/usr/bin/python3
"""
This module contains object imports common to all modules in the test paackage
"""
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from test.test_database.test_models.test_category import cat_obj
from test.test_database.test_models.test_inventory import inv_obj
from test.test_database.test_models.test_inven_transaction import inv_trans_obj
from test.test_database.test_models.test_inven_transaction import (
    inv_trans_kwargs_with_inv_id,
)
from test.test_database.test_models.test_product import prod_obj
from test.test_database.test_models.test_product import prod_kwarg_with_cat_id
from test.test_database.test_models.test_inventory import (
    inv_kwargs_with_prod_id,
)


# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


# Create test session
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=_engine
)
