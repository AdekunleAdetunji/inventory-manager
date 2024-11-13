#!/usr/bin/env python3

"""
This module contains test functions for the BaseModel class
"""
import pytest
from datetime import datetime
from main.database.models.basemodel import BaseModel


class BaseModels(BaseModel):
    __tablename__ = "basemodels"
    pass


@pytest.fixture
def basemodel_inst(db_session):
    """create a new mapped user object"""
    inst = BaseModels()
    db_session.add(inst)
    db_session.commit()
    return inst


def test_basemodel_add(basemodel_inst):
    """test basemodel object successful initialization and commit to database"""
    assert (
        basemodel_inst.id and basemodel_inst.created and basemodel_inst.updated
    )


def test_basemodel_to_dict(basemodel_inst):
    """test basemodel instance to_dict method"""
    inst_dict = basemodel_inst.to_dict()
    assert inst_dict and isinstance(inst_dict, dict) and len(inst_dict) == 3
    assert (
        basemodel_inst.id == inst_dict["id"]
        and datetime.strptime(inst_dict["created"], "%Y-%m-%dT%H:%M:%S")
        and datetime.strptime(inst_dict["updated"], "%Y-%m-%dT%H:%M:%S")
    )


def test_basemodel__str__(basemodel_inst):
    """
    test that basemodel __str__ method print a human readable representation
    of the object
    """
    assert str(basemodel_inst)


def test_basemodel__repr__(basemodel_inst):
    """
    test that basemodel __str__ method print a machine readable representation
    of the object
    """
    assert repr(basemodel_inst)
