#!/usr/bin/python3
"""
This module contains tests for the pydantic inventory model validators
"""
import pytest
from main.validators.inventory import InventoryRequestValidator
from main.validators.inventory import InventoryResponseValidator
from pydantic import ValidationError
from test import *


def test_inv_req_val_init_success(inv_kwargs_with_prod_id):
    """
    test that InventoryRequestValidator initializes correctly
    """
    req_obj = InventoryRequestValidator(**inv_kwargs_with_prod_id)
    assert req_obj.country and req_obj.quantity and req_obj.product_id


def test_inv_res_val_init_success(inv_obj):
    """
    test that InventoryResponseValidator initializes correctly
    """
    res_obj = InventoryResponseValidator.model_validate(inv_obj)
    assert (
        res_obj.id
        and res_obj.created
        and res_obj.updated
        and res_obj.country
        and res_obj.quantity
        and res_obj.product_id
        and not res_obj.transactions
    )


def test_inv_res_val_init_with_inv_trans_success(inv_trans_obj):
    """
    test that InventoryResponseValidator initializes when supplied an inv_obj
    with inventory transactions
    """
    # obtain inventory object linked to an inventorytransaction
    inv_obj = inv_trans_obj.inventory

    res_obj = InventoryResponseValidator.model_validate(inv_obj)
    assert res_obj.transactions


def test_inv_req_init_fail_no_prod_id(inv_kwargs):
    """
    test that inventory model request validator fails when instantiatied with
    empty product_id
    """
    # delete the product_id field value of the inv_kwargs
    del inv_kwargs["product_id"]
    with pytest.raises(ValidationError) as val_err_obj:
        InventoryRequestValidator(**inv_kwargs)
    assert "missing" in str(val_err_obj.value)


def test_inv_req_init_fail_no_quantity(inv_kwargs_with_prod_id):
    """
    test that initialization of InventoryRequestValidator fails when initialized
    with no quantity field value
    """
    # delete the quantity field value of the inv_kwargs
    del inv_kwargs_with_prod_id["quantity"]
    with pytest.raises(ValidationError) as val_err_obj:
        InventoryRequestValidator(**inv_kwargs_with_prod_id)
    assert "missing" in str(val_err_obj.value)


def test_inv_req_init_fail_no_country(inv_kwargs_with_prod_id):
    """
    test that initialization of InventoryRequestValidator fails when initialized
    with no country field value
    """
    # delete the country field value of the inv_kwargs
    del inv_kwargs_with_prod_id["country"]
    with pytest.raises(ValidationError) as val_err_obj:
        InventoryRequestValidator(**inv_kwargs_with_prod_id)
    assert "missing" in str(val_err_obj.value)


def test_inv_req_init_fail_type_product_id(inv_kwargs_with_prod_id):
    """
    test that initialization of InventoryRequestValidator fails when initialized
    with the wrong product_id type
    """
    # assign a string value to the product_id inv_kwargs_with_prod_id field
    inv_kwargs_with_prod_id["product_id"] = "uuid"
    with pytest.raises(ValidationError) as val_err_obj:
        InventoryRequestValidator(**inv_kwargs_with_prod_id)
    assert "uuid_parsing" in str(val_err_obj.value)


def test_inv_req_init_fail_type_coutry(inv_kwargs_with_prod_id):
    """
    test that initialization of InventoryRequestValidator fails when initialized
    with the invalid country code
    """
    # assign an integer value to the country inv_kwargs_with_prod_id field
    inv_kwargs_with_prod_id["country"] = 23
    with pytest.raises(ValidationError) as val_err_obj:
        InventoryRequestValidator(**inv_kwargs_with_prod_id)
    assert "string_type" in str(val_err_obj.value)


def test_inv_req_init_fail_type_quantity(inv_kwargs_with_prod_id):
    """
    test that initialization of InventoryRequestValidator fails when initialized
    with invalid quantity field type
    """
    # assign an string value to the quantity inv_kwargs_with_prod_id field
    inv_kwargs_with_prod_id["quantity"] = "five"
    with pytest.raises(ValidationError) as val_err_obj:
        InventoryRequestValidator(**inv_kwargs_with_prod_id)
    assert "int_parsing" in str(val_err_obj.value)
