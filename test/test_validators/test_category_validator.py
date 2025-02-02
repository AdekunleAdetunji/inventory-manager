#!/usr/bin/env python3
"""
This module contains tests for the category model request and response body
validator models
"""
import pytest
from main.validators.category import CategoryRequestValidator
from main.validators.category import CategoryResponseValidator
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
    )


@pytest.mark.val_err_obj_fixt_data(
    "missing",
    CategoryRequestValidator,
    "cat_kwargs",
    "name",
)
def test_cat_req_val_init_fail_no_name(val_err_obj):
    """
    test that a validation error is raised as a result of initialization
    with no name field value
    """
    assert "missing" in str(val_err_obj.value)


@pytest.mark.val_err_obj_fixt_data(
    "missing",
    CategoryRequestValidator,
    "cat_kwargs",
    "code",
)
def test_cat_req_val_init_fail_no_code(val_err_obj):
    """
    test that a validation error is raised as a result of initialization
    with no code field value
    """
    assert "missing" in str(val_err_obj.value)


@pytest.mark.val_err_obj_fixt_data(
    "missing",
    CategoryRequestValidator,
    "cat_kwargs",
    "description",
)
def test_cat_req_val_init_fail_no_description(val_err_obj):
    """
    test that a validation error is raised as a result of initialization
    with no description field value
    """
    assert "missing" in str(val_err_obj.value)


@pytest.mark.val_err_obj_fixt_data(
    "type",
    CategoryRequestValidator,
    "cat_kwargs",
    "name",
    {},
)
def test_cat_req_val_init_fail_inv_name(val_err_obj):
    """
    test that a validation error is raised as a result of initialization
    with wrong name field value type
    """
    assert "string_type" in str(val_err_obj.value)


@pytest.mark.val_err_obj_fixt_data(
    "type",
    CategoryRequestValidator,
    "cat_kwargs",
    "code",
    ["a"],
)
def test_cat_req_val_init_fail_inv_code(val_err_obj):
    """
    test that a validation error is raised as a result of initialization
    with wrong code field value type
    """
    assert "string_type" in str(val_err_obj.value)


@pytest.mark.val_err_obj_fixt_data(
    "type",
    CategoryRequestValidator,
    "cat_kwargs",
    "description",
    3,
)
def test_cat_req_val_init_fail_inv_description(val_err_obj):
    """
    test that a validation error is raised as a result of initialization
    with wrong description field value type
    """
    assert "string_type" in str(val_err_obj.value)
