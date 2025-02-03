#!/usr/bin/env python3
"""
This module contains tests for the product model request and response body
validator models
"""
import pytest
from main.validators.product import ProductRequestValidator
from main.validators.product import ProductResponseValidator
from pydantic import ValidationError
from test import *


def test_prod_req_val_init_success(prod_kwarg_with_cat_id):
    """
    test that the product request validator pydantic model initializes
    properly
    """
    req_obj = ProductRequestValidator(**prod_kwarg_with_cat_id)
    assert req_obj


def test_prod_res_val_init_success(prod_obj):
    """
    test that the product response validator pydantic model initializes
    properly
    """
    # dictionary representation of a product in the products table
    res_obj = ProductResponseValidator.model_validate(prod_obj)
    assert (
        res_obj.id
        and res_obj.created
        and res_obj.updated
        and res_obj.category_id
        and res_obj.name
        and res_obj.price
        and res_obj.is_active
        and not res_obj.inventories
    )


def test_prod_res_val_init_success_with_inv(inv_obj):
    """
    test that ProductResponseValidator initializes when supplied a Product
    instance linked to an inventory object
    """
    # obtain the product object linked to an inventory object
    prod_obj = inv_obj.product

    res_obj = ProductResponseValidator.model_validate(prod_obj)
    assert res_obj.inventories


def test_req_val_init_fail_no_name(prod_kwarg_with_cat_id):
    """
    test that pydantic ProductRequestValidator model raises a Validation error
    when instantiated with no name field value
    """
    # delete name key from prod_kwarg_with_cat_id
    del prod_kwarg_with_cat_id["name"]
    with pytest.raises(ValidationError) as val_err_obj:
        ProductRequestValidator(**prod_kwarg_with_cat_id)
    assert "missing" in str(val_err_obj.value)


def test_req_val_init_fail_no_sku(prod_kwarg_with_cat_id):
    """
    test that pydantic ProductRequestValidator model raises a Validation error
    when instantiated with no sku field value
    """
    # delete "sku" key from prod_kwarg_with_cat_id
    del prod_kwarg_with_cat_id["sku"]
    with pytest.raises(ValidationError) as val_err_obj:
        ProductRequestValidator(**prod_kwarg_with_cat_id)
    assert "missing" in str(val_err_obj.value)


def test_req_obj_init_fail_no_price(prod_kwarg_with_cat_id):
    """
    test that pydantic ProductRequestValidator model raises a Validation error
    when instantiated with no price field value
    """
    # delete "price" key from prod_kwarg_with_cat_id
    del prod_kwarg_with_cat_id["price"]
    with pytest.raises(ValidationError) as val_err_obj:
        ProductRequestValidator(**prod_kwarg_with_cat_id)
    assert "missing" in str(val_err_obj.value)


def test_req_obj_init_fail_no_cat_id(prod_kwarg_with_cat_id):
    """
    test that pydantic ProductRequestValidator model raises a Validation error
    when instantiated with no category_id field value
    """
    # delete "cat_idk" key from prod_kwarg_with_cat_id
    del prod_kwarg_with_cat_id["category_id"]
    with pytest.raises(ValidationError) as val_err_obj:
        ProductRequestValidator(**prod_kwarg_with_cat_id)
    assert "missing" in str(val_err_obj.value)


def test_req_obj_init_fail_type_name(prod_kwarg_with_cat_id):
    """
    test that pydantic ProductRequestValidator model raises a Validation error
    when instantiated with wrong name field value type
    """
    # assign a list literal to prod_kwarg_with_cat_id["name"] kwy
    prod_kwarg_with_cat_id["name"] = []
    with pytest.raises(ValidationError) as val_err_obj:
        ProductRequestValidator(**prod_kwarg_with_cat_id)
    assert "string_type" in str(val_err_obj.value)


@pytest.mark.val_err_obj_fixt_data(
    "type",
    ProductRequestValidator,
    "prod_kwargs",
    "sku",
    [],
)
def test_req_obj_init_fail_type_sku(prod_kwarg_with_cat_id):
    """
    test that pydantic ProductRequestValidator model raises a Validation error
    when instantiated with wrong sku field value type
    """
    # assign a integer literal to prod_kwarg_with_cat_id["sku"] key
    prod_kwarg_with_cat_id["sku"] = 12
    with pytest.raises(ValidationError) as val_err_obj:
        ProductRequestValidator(**prod_kwarg_with_cat_id)
    assert "string_type" in str(val_err_obj.value)


def test_req_obj_init_fail_type_price(prod_kwarg_with_cat_id):
    """
    test that pydantic ProductRequestValidator model raises a Validation error
    when instantiated with wrong sku field value type
    """
    # assign a string literal to prod_kwarg_with_cat_id["sku"] key
    prod_kwarg_with_cat_id["price"] = "hsl"
    with pytest.raises(ValidationError) as val_err_obj:
        ProductRequestValidator(**prod_kwarg_with_cat_id)
    assert "float_parsing" in str(val_err_obj.value)
