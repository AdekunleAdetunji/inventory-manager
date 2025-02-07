#!/usr/bin/python3
"""
This module contains testsuites for the admin ORM validator model
"""
import pytest
from main.validators.admin import AdminRequestValidator
from main.validators.admin import AdminResponseValidator
from pydantic import ValidationError
from test import *


def test_admin_req_val_init_success(admin_kwargs):
    """
    test that the admin request validator model initializes successfully with
    all field values provided
    """
    req_obj = AdminRequestValidator(**admin_kwargs)
    assert (
        req_obj.email
        and req_obj.password
        and req_obj.first_name
        and req_obj.last_name
    )


def test_admin_res_val_init_success(admin_obj):
    """
    test that the admin response validator model initializes successfully with
    all field values provided
    """
    res_obj = AdminResponseValidator.model_validate(admin_obj)
    assert (
        res_obj.id
        and res_obj.created
        and res_obj.updated
        and res_obj.email
        and res_obj.first_name
        and res_obj.last_name
    )


def test_admin_req_val_init_fail_no_email(admin_kwargs):
    """
    test that AdminRequestValidator  fails when no email field value is
    provided
    """
    # remove email key from admin_kwargs
    del admin_kwargs["email"]
    with pytest.raises(ValidationError) as val_err_obj:
        AdminRequestValidator(**admin_kwargs)
    assert "missing" in str(val_err_obj.value)


def test_admin_req_val_init_fail_no_password(admin_kwargs):
    """
    test that AdminRequestValidator initialization fails when no password field
    value is provided
    """
    # remove password key from admin_kwargs
    del admin_kwargs["password"]
    with pytest.raises(ValidationError) as val_err_obj:
        AdminRequestValidator(**admin_kwargs)
    assert "missing" in str(val_err_obj.value)


def test_admin_req_val_init_fail_no_first_name(admin_kwargs):
    """
    test that AdminRequestValidator initialization fails when no first_name field
    value is provided
    """
    # remove first_name key from admin_kwargs
    del admin_kwargs["first_name"]
    with pytest.raises(ValidationError) as val_err_obj:
        AdminRequestValidator(**admin_kwargs)
    assert "missing" in str(val_err_obj.value)


def test_admin_req_val_init_fail_no_last_name(admin_kwargs):
    """
    test that AdminRequestValidator initialization fails when no last_name field
    value is provided
    """
    # remove last_name key from admin_kwargs
    del admin_kwargs["last_name"]
    with pytest.raises(ValidationError) as val_err_obj:
        AdminRequestValidator(**admin_kwargs)
    assert "missing" in str(val_err_obj.value)


def test_admin_req_val_init_fail_inv_email(admin_kwargs):
    """
    test that AdminRequestValidator fails when initialized with the wrong email
    field value
    """
    # assign to the admin_kwargs email key a plain string
    admin_kwargs["email"] = "admin"
    with pytest.raises(ValidationError) as val_err_obj:
        AdminRequestValidator(**admin_kwargs)
    assert "value_error" in str(val_err_obj.value)


def test_admin_req_val_init_fail_inv_password(admin_kwargs):
    """
    test that AdminRequestValidator fails when initialized with the wrong
    password field value
    """
    # assign to the admin_kwargs password key a integer literal
    admin_kwargs["password"] = 2345
    with pytest.raises(ValidationError) as val_err_obj:
        AdminRequestValidator(**admin_kwargs)
    assert "string_type" in str(val_err_obj.value)


def test_admin_req_val_init_fail_inv_first_name(admin_kwargs):
    """
    test that AdminRequestValidator fails when initialized with the wrong
    first_name field value
    """
    # assign to the admin_kwargs password key a list
    admin_kwargs["first_name"] = list("abc")
    with pytest.raises(ValidationError) as val_err_obj:
        AdminRequestValidator(**admin_kwargs)
    assert "string_type" in str(val_err_obj.value)


def test_admin_req_val_init_fail_inv_last_name(admin_kwargs):
    """
    test that AdminRequestValidator fails when initialized with the wrong
    last_name field value
    """
    # assign to the admin_kwargs last_name key a dictionary
    admin_kwargs["last_name"] = {"a": "b"}
    with pytest.raises(ValidationError) as val_err_obj:
        AdminRequestValidator(**admin_kwargs)
    assert "string_type" in str(val_err_obj.value)
