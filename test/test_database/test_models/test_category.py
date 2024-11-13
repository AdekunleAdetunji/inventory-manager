#!/usr/bin/env python3
"""
This module contains tests for the category sqlalchemy orm
"""
import pytest
from main.database.models.category import Category
from main.database.models.product import Product


@pytest.fixture()
def cat_obj(db_session, cat_kwargs):
    """
    fixture to instantiate a category model, add and commit it to db_session
    and delete it after the session
    """
    obj = Category(**cat_kwargs)
    db_session.add(obj)
    db_session.commit()

    yield obj

    db_session.delete(obj)
    db_session.commit()


def test_cat_inst_success(cat_obj):
    """test if category object successfully instantiated with all attributes"""
    # check that all attribute are correctely initialized and populated
    assert (
        cat_obj
        and cat_obj.id
        and cat_obj.created
        and cat_obj.updated
        and cat_obj.code
        and cat_obj.description
        and cat_obj.name
        and not cat_obj.products
    )


def test_cat_prod_attr(cat_obj, prod_kwargs, db_session):
    """test if category model links with a product model object"""
    cat_obj.products.append(Product(**prod_kwargs))
    db_session.commit()
    assert cat_obj.products[0].category_id == cat_obj.id


# pass fixture data to the missing_arg_error fixture
@pytest.mark.missing_arg_error_fixt_data(Category, "cat_kwargs", "name")
def test_cat_inst_missing_name_attr(missing_arg_error):
    """test initialization of a category model with no name attribute value"""
    assert "NOT NULL constraint failed: category.name" in str(
        missing_arg_error.value
    )


# pass fixture data to the missing_arg_error fixture
@pytest.mark.missing_arg_error_fixt_data(Category, "cat_kwargs", "code")
def test_cat_inst_missing_code_attr(missing_arg_error):
    """test initialization of a category model with no code value"""
    assert "NOT NULL constraint failed: category.code" in str(
        missing_arg_error.value
    )


# pass fixture data to the missing_arg_error fixture
@pytest.mark.missing_arg_error_fixt_data(Category, "cat_kwargs", "description")
def test_cat_inst_mission_desc_attr(missing_arg_error):
    """test initialization of a category model with no desc field provided"""
    assert "NOT NULL constraint failed: category.description" in str(
        missing_arg_error.value
    )
