#!/usr/bin/env python3
"""
This model contains tests for the inventory transaction orm model
"""
import pytest
from main.database.models.inven_transaction import InventoryTransaction
from test.test_database.test_models.test_category import cat_obj
from test.test_database.test_models.test_inventory import inv_obj
from test.test_database.test_models.test_product import prod_obj


@pytest.fixture()
def inv_trans_obj(db_session, inv_obj, inv_trans_kwargs):
    """fixture to yield an inventory transaction model object"""
    inv_trans_obj = InventoryTransaction(**inv_trans_kwargs)
    inv_obj.transactions.append(inv_trans_obj)
    db_session.commit()

    yield inv_trans_obj

    db_session.delete(inv_trans_obj)
    db_session.commit()


@pytest.fixture()
def inv_trans_kwargs_with_inv_id(inv_trans_kwargs, inv_obj):
    """
    fixture to return a dictionary of inventory transaction model instance
    kwargs with inventory_id key value pair
    """
    inv_trans_kwargs["inventory_id"] = inv_obj.id

    return inv_trans_kwargs


def test_inv_trans_obj_init_success(inv_trans_obj):
    """
    test that inventory transaction object is successfully initialized and
    commited to the database
    """
    assert (
        inv_trans_obj
        and inv_trans_obj.id
        and inv_trans_obj.created
        and inv_trans_obj.updated
        and inv_trans_obj.quantity
    )


@pytest.mark.missing_arg_error_fixt_data(
    InventoryTransaction, "inv_trans_kwargs_with_inv_id", "quantity"
)
def test_inv_init_fail_no_quantity_key_value(missing_arg_error):
    """
    test instantiation of inventory transaction model with plain kwargs dictionary
    without quantity key value
    """
    assert "NOT NULL constraint failed: inventory_transaction.quantity" in str(
        missing_arg_error.value
    )
