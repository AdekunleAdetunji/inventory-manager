#!/usr/bin/python3
"""
This module contains testsuites for the database admin sqlalchemy orm
"""
import pytest
from main.database.models.admin import Admin


@pytest.fixture()
def admin_obj(db_session, admin_kwargs):
    """
    fixture to instantiate an admin model, add and commit it to db_session
    and delete it after the session
    """
    admin_obj = Admin(**admin_kwargs)
    db_session.add(admin_obj)
    db_session.commit()

    yield admin_obj

    db_session.delete(admin_obj)
    db_session.commit()


def test_admin_init_success(admin_obj):
    """
    test that admin model instance initializes successfully with all required
    instance attributes provided
    """
    assert (
        admin_obj
        and admin_obj.id
        and admin_obj.created
        and admin_obj.updated
        and admin_obj.email
        and admin_obj.password
        and admin_obj.first_name
        and admin_obj.last_name
    )


@pytest.mark.missing_arg_error_fixt_data(Admin, "admin_kwargs", "email")
def test_admin_init_fail_no_email(missing_arg_error):
    """
    test that initialization of Admin model fails with no email instance
    attribute value provided
    """
    assert "NOT NULL constraint failed: admin.email" in str(
        missing_arg_error.value
    )


@pytest.mark.missing_arg_error_fixt_data(Admin, "admin_kwargs", "password")
def test_admin_init_fail_no_password(missing_arg_error):
    """
    test that initialization of Admin model fails with no password instance
    attribute value provided
    """
    assert "NOT NULL constraint failed: admin.password" in str(
        missing_arg_error.value
    )


@pytest.mark.uniq_const_error_fixt_data(Admin, "admin_kwargs")
def test_admin_init_fail_dual_email(uniq_const_error):
    """
    test that commit fails when there is an admin object with same email
    """
    assert "UNIQUE constraint failed" in str(uniq_const_error.value)
