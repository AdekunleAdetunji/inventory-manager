#!/usr/bin/env python3
"""
This module contains tests for the sqlalchemy product orm model
"""
import pytest
from main.database.models.product import Product
from test.test_database.test_models.test_category import cat_obj


@pytest.fixture()
def prod_kwarg_with_cat_id(prod_kwargs, cat_obj):
    """
    fixture to return a dictionary of product model instance kwargs with
    category_id key:value pair
    """
    # update prod_kwargs with category object id
    prod_kwargs["category_id"] = cat_obj.id

    return prod_kwargs


@pytest.fixture()
def prod_obj(db_session, prod_kwargs, cat_obj):
    """
    fixture to instantiate a prod model, add and commit it to db_session
    and delete it after the session
    """
    cat_obj.products.append(Product(**prod_kwargs))
    db_session.commit()

    yield cat_obj.products[0]


def test_prod_init_success(prod_obj):
    """
    test that product object is successfully initialized and commited to the
    database
    """
    assert (
        prod_obj.id
        and prod_obj.created
        and prod_obj.updated
        and prod_obj.name
        and prod_obj.sku
        and prod_obj.price
        and not prod_obj.description
    )


@pytest.mark.missing_arg_error_fixt_data(Product, "prod_kwargs", "category_id")
def test_prod_init_fail_no_cat_id_key_value(missing_arg_error):
    """
    test that initialization fails when no category_id kwargs is provided and
    the product object is not linked to any class
    """
    assert "NOT NULL constraint failed: product.category_id" in str(
        missing_arg_error.value
    )


@pytest.mark.missing_arg_error_fixt_data(
    Product, "prod_kwarg_with_cat_id", "name"
)
def test_prod_init_fail_no_name_key_value(missing_arg_error):
    """
    test that initialization of a product model fail with empty "name"
    attribute value
    """
    assert "NOT NULL constraint failed: product.name" in str(
        missing_arg_error.value
    )


@pytest.mark.missing_arg_error_fixt_data(
    Product, "prod_kwarg_with_cat_id", "sku"
)
def test_prod_init_fail_no_sku_key_value(missing_arg_error):
    """
    test that initialization of a product model fail with empty "sku"
    attribute value
    """
    assert "NOT NULL constraint failed: product.sku" in str(
        missing_arg_error.value
    )


@pytest.mark.missing_arg_error_fixt_data(
    Product, "prod_kwarg_with_cat_id", "price"
)
def test_prod_init_fail_no_price_key_value(missing_arg_error):
    """
    test that initialization of a product model fail with empty "price"
    attribute value
    """
    assert "NOT NULL constraint failed: product.price" in str(
        missing_arg_error.value
    )


@pytest.mark.missing_arg_error_fixt_data(
    Product, "prod_kwarg_with_cat_id", "category_id"
)
def test_prod_init_fail_no_cat_id_key_value(missing_arg_error):
    """
    test that initialization of a product model fail with empty "category_id"
    attribute value
    """
    assert "NOT NULL constraint failed: product.category_id" in str(
        missing_arg_error.value
    )


@pytest.mark.uniq_const_error_fixt_data(Product, "prod_kwarg_with_cat_id")
def test_prod_init_fail_dual_name_val(uniq_const_error):
    """
    test that commiting two product models fail due to a unique column
    having repeating values fails
    """
    assert "UNIQUE constraint failed" in str(uniq_const_error.value)
