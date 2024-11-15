#!/usr/bin/env python3
"""
This module contains tests for the inventory orm
"""
import pytest
from main.database.models.inventory import Inventory
from test.test_database.test_models.test_category import cat_obj
from test.test_database.test_models.test_product import prod_obj


@pytest.fixture()
def inv_obj(db_session, prod_obj, inv_kwargs):
    """
    fixture to instantiate an inventory model, add and commit it to a
    database session and delete it after the session
    """

    inv_obj = Inventory(**inv_kwargs)
    prod_obj.inventories.append(inv_obj)
    db_session.commit()
    # inv_obj = prod_obj.inventories[0]

    yield inv_obj

    db_session.delete(inv_obj)
    db_session.commit()


@pytest.fixture()
def inv_kwargs_with_prod_id(inv_kwargs, prod_obj):
    """
    fixture to return a dictionary of inventory model instance kwargs with
    product_id value
    """
    inv_kwargs["product_id"] = prod_obj.id

    return inv_kwargs


def test_inv_init_success(inv_obj):
    """
    test that inventory object is successfully initialized and commited to the
    database
    """
    assert (
        inv_obj.id
        and inv_obj.created
        and inv_obj.updated
        and inv_obj.country
        and inv_obj.quantity
        and inv_obj.product_id
    )


@pytest.mark.missing_arg_error_fixt_data(Inventory, "inv_kwargs", "product_id")
def test_inv_init_fail_no_prod_id_key_value(missing_arg_error):
    """
    test instantiation of inventory model with plain kwargs dictionary without
    product_id key value
    """
    assert "NOT NULL constraint failed: inventory.product_id" in str(
        missing_arg_error.value
    )


@pytest.mark.missing_arg_error_fixt_data(
    Inventory, "inv_kwargs_with_prod_id", "country"
)
def test_inv_init_fail_no_country_key_value(missing_arg_error):
    """
    test instantiation of inventory model with plain kwargs dictionary
    without country key value
    """
    assert "NOT NULL constraint failed: inventory.country" in str(
        missing_arg_error.value
    )


@pytest.mark.missing_arg_error_fixt_data(
    Inventory, "inv_kwargs_with_prod_id", "quantity"
)
def test_inv_init_fail_no_quantity_key_value(missing_arg_error):
    """
    test instantiation of inventory model with plain kwargs dictionary
    without quantity key value
    """
    assert "NOT NULL constraint failed: inventory.quantity" in str(
        missing_arg_error.value
    )
