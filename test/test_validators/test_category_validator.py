#!/usr/bin/env python3
"""
This module contains tests for the category model request and response body
validator models
"""
import pytest
from main.validators.category import CategoryRequestValidator
from main.validators.category import CategoryResponseValidator
from pydantic import ValidationError
from test import *


def test_cat_req_val_init_success(cat_kwargs):
    """
    test that the category request validator pydantic model initializes
    properly
    """
    req_obj = CategoryRequestValidator(**cat_kwargs)
    assert req_obj.name and req_obj.code and req_obj.description


def test_cat_res_val_init_success(cat_obj):
    """
    test that the category response object correctly initializes from a database
    category model object
    """
    res_obj = CategoryResponseValidator.model_validate(cat_obj)
    assert (
        res_obj.id
        and res_obj.created
        and res_obj.updated
        and res_obj.name
        and res_obj.code
        and res_obj.description
        and not res_obj.products
    )


def test_cat_res_val_init_success_with_product(prod_obj):
    """
    test that CategoryResponseValidator instantiates when supplied an category
    instance with products field
    """
    # obtain category object linked to a product
    cat_obj = prod_obj.category

    res_obj = CategoryResponseValidator.model_validate(cat_obj)
    assert res_obj.products


def test_cat_req_val_init_fail_no_name(cat_kwargs):
    """
    test that a validation error is raised as a result of initialization
    with no name field value
    """
    # delete name key from cat_kwargs
    del cat_kwargs["name"]
    with pytest.raises(ValidationError) as val_err_obj:
        CategoryRequestValidator(**cat_kwargs)
    assert "missing" in str(val_err_obj.value)


def test_cat_req_val_init_fail_no_code(cat_kwargs):
    """
    test that a validation error is raised as a result of initialization
    with no code field value
    """
    # delete code key from cat_kwargs
    del cat_kwargs["code"]
    with pytest.raises(ValidationError) as val_err_obj:
        CategoryRequestValidator(**cat_kwargs)
    assert "missing" in str(val_err_obj.value)


def test_cat_req_val_init_fail_no_description(cat_kwargs):
    """
    test that a validation error is raised as a result of initialization
    with no description field value
    """
    # delete description key from cat_kwargs
    del cat_kwargs["description"]
    with pytest.raises(ValidationError) as val_err_obj:
        CategoryRequestValidator(**cat_kwargs)
    assert "missing" in str(val_err_obj.value)


def test_cat_req_val_init_fail_inv_name(cat_kwargs):
    """
    test that a validation error is raised as a result of initialization
    with wrong name field value type
    """
    # assign an integer value to the name key of cat_kwargs
    cat_kwargs["name"] = 12
    with pytest.raises(ValidationError) as val_err_obj:
        CategoryRequestValidator(**cat_kwargs)
    assert "string_type" in str(val_err_obj.value)


def test_cat_req_val_init_fail_inv_code(cat_kwargs):
    """
    test that a validation error is raised as a result of initialization
    with wrong code field value type
    """
    # assign a list value to the code field of cat_kwargs
    cat_kwargs["code"] = list("123")
    with pytest.raises(ValidationError) as val_err_obj:
        CategoryRequestValidator(**cat_kwargs)
    assert "string_type" in str(val_err_obj.value)


def test_cat_req_val_init_fail_inv_description(cat_kwargs):
    """
    test that a validation error is raised as a result of initialization
    with wrong description field value type
    """
    # assign a dictionary value to the description key in cat_kwargs
    cat_kwargs["description"] = {1: 2, "a": "b"}
    with pytest.raises(ValidationError) as val_err_obj:
        CategoryRequestValidator(**cat_kwargs)
    assert "string_type" in str(val_err_obj.value)
