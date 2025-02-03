#!/usr/bin/python3
"""
This module configures pytest globally, making fixtures and others available
for testing
"""
import pytest
from main.database.engine import db_engine
from sqlalchemy import exc
from sqlalchemy.orm import Session


def pytest_addoption(parser):
    """Configure pytest to recieve custom command line argument"""
    parser.addoption(
        "--db_url",
        action="store",
        default="sqlite://",
        help="kindly provide command line argument specifying the database url",
    )


def pytest_configure(config):
    """configure pytest to recognize new markers"""

    config.addinivalue_line(
        "markers",
        "missing_arg_error_fixt_data",
    )  # suppress pytest unrecognized marker warning
    config.addinivalue_line(
        "markers",
        "uniq_const_error_fixt_data",
    )  # suppress pytest unrecognized marker marker warning
    config.addinivalue_line(
        "markers",
        "val_err_obj_fixt_data",
    )  # suppress pytest unrecognized marker marker warning


@pytest.fixture(autouse=True)
def db_session():
    """
    yield a database session that is rolled back after each test
    """
    _engine = db_engine()
    _session = Session(bind=db_engine())

    yield _session

    # dispose the created engine
    _engine.dispose()
    _session.close()


@pytest.fixture()
def cat_kwargs() -> dict:
    """
    fixture to return a dictionary of attribute key and values to be used in
    instantiating a category model
    """
    # a dictionary of complete category model instance attribute values
    return {
        "name": "complete",
        "code": "COMP",
        "description": "This is the category for electronic appliances",
    }


@pytest.fixture()
def prod_kwargs() -> dict:
    """
    fixture to return a dictionary of product model attribute values required
    to instantiate a product model object
    """

    return {
        "name": "Sony",
        "sku": "12344556",
        "price": 12.0,
        "category_id": "",
    }


@pytest.fixture()
def inv_kwargs() -> dict:
    """
    fixture to return a dictionary of inventory model attribute values required
    to instantiate an inventory model object
    """
    return {"country": "US", "quantity": 3, "product_id": ""}


@pytest.fixture()
def inv_trans_kwargs() -> dict:
    """
    fixture to return a dictionary of inventory transaction model attribute
    values required to instantiate an inventory model object
    """
    return {
        "quantity": 3,
    }


@pytest.fixture()
def missing_arg_error(request, db_session):
    """fixture to return a sqlalchemy not null constraint error object"""
    with pytest.raises(exc.IntegrityError) as err_obj:
        # obtain fixture marker object
        marker = request.node.get_closest_marker("missing_arg_error_fixt_data")

        # assign the orm model class to the model variable
        model = marker.args[0]

        # get the name of kwargs fixture
        kwargs_fixt_name = marker.args[1]
        # get the fixture value
        kwargs = request.getfixturevalue(kwargs_fixt_name)

        # obtain name of argument to be deleted from kwargs
        arg_name = marker.args[2]

        del kwargs[arg_name]

        model_obj = model(**kwargs)
        db_session.add(model_obj)
        db_session.commit()

    yield err_obj

    # rollback session
    db_session.rollback()


@pytest.fixture()
def uniq_const_error(request, db_session):
    """fixture to return a unique key constraint fail error object"""
    with pytest.raises(exc.IntegrityError) as err_obj:
        # getthe marker supplying data to be used by fixture
        marker = request.node.get_closest_marker("uniq_const_error_fixt_data")
        # obtain the sqlalchemy orm model
        model = marker.args[0]
        # obtain the kwargs to be used in model initialization
        kwargs_fixt_name = marker.args[1]
        # get the fixture value
        kwargs = request.getfixturevalue(kwargs_fixt_name)
        # initialize models
        obj_1 = model(**kwargs)
        obj_2 = model(**kwargs)
        db_session.add_all([obj_1, obj_2])
        db_session.commit()

    # yield error object to test function
    yield err_obj

    # rollback faiiled transaction
    db_session.rollback()
