#!/usr/bin/python3
"""
This module contains tests for the InventoryTransaction pydantic validator
"""
import pytest
from main.validators.inventory_transaction import (
    InventoryTransactionRequestValidator,
)
from main.validators.inventory_transaction import (
    InventoryTransactionResponseValidator,
)
from pydantic import ValidationError
from test import *
from uuid import uuid4


def test_inv_trans_req_val_init_success(inv_trans_kwargs):
    """
    test that InventoryTransactionRequestValidator instantiates properly
    """
    inv_trans_kwargs["inventory_id"] = uuid4()
    req_obj = InventoryTransactionRequestValidator(**inv_trans_kwargs)
    assert req_obj.inventory_id and req_obj.quantity


def test_inv_trans_res_val_init_success(inv_trans_obj):
    """test that InventoryTransactionResponseValidator instantiates properly"""
    res_obj = InventoryTransactionResponseValidator.model_validate(
        inv_trans_obj
    )
    assert (
        res_obj.id
        and res_obj.created
        and res_obj.updated
        and res_obj.inventory_id
        and res_obj.quantity
    )


def test_inv_trans_req_val_no_inv_id(inv_trans_kwargs):
    """
    test that InventoryTransactionRequestValidator fails when instantiated with
    no inventory_id field value
    """
    with pytest.raises(ValidationError) as VE:
        InventoryTransactionRequestValidator(**inv_trans_kwargs)
    assert "missing" in str(VE.value)


def test_inv_trans_req_val_no_quantity(inv_trans_kwargs_with_inv_id):
    """
    test that InventoryTransactionRequestValidator fails when instantiated with
    no quantity field value
    """
    # delete quantity key from inv_trans_kwargs_with_inv_id
    del inv_trans_kwargs_with_inv_id["quantity"]
    with pytest.raises(ValidationError) as VE:
        InventoryTransactionRequestValidator(**inv_trans_kwargs_with_inv_id)
    assert "missing" in str(VE.value)


def test_inv_trans_req_val_type_inv_id(inv_trans_kwargs):
    """
    test that InventoryTransactionRequestValidator fails when instantiated with
    the wrong inventory_id field value type
    """
    # assign a string literal to inv_trans_kwargs["inventory_id"] kwy
    inv_trans_kwargs["inventory_id"] = "uuid"
    with pytest.raises(ValidationError) as VE:
        InventoryTransactionRequestValidator(**inv_trans_kwargs)
    assert "uuid_parsing" in str(VE.value)


def test_inv_trans_req_val_type_quantity(inv_trans_kwargs_with_inv_id):
    """
    test that InventoryTransactionRequestValidator fails when instantiated with
    the wrong inventory_id field value type
    """
    # assign a list literal to inv_trans_kwargs["quantity"] kwy
    inv_trans_kwargs_with_inv_id["quantity"] = list("123")
    with pytest.raises(ValidationError) as VE:
        InventoryTransactionRequestValidator(**inv_trans_kwargs_with_inv_id)
    assert "int_type" in str(VE.value)
