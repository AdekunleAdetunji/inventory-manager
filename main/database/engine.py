#!/usr/bin/env python3

"""
This module contains function definitions to allow transactions on postgresql
database tables
"""
from main.database.base import Base
from main.validators.config import get_db_env_vars
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


# obtain validated database environment variables
db_vars = get_db_env_vars()


def db_engine():
    """
    Database engine to be used to establish connection with postgresql
    database
    """

    db_url = (
        "postgresql://"
        + f"{db_vars.DB_USER}:{db_vars.DB_PASSWORD}"
        + f"@{db_vars.DB_HOST}:{db_vars.DB_PORT}/"
        + f"{db_vars.DB_NAME}"
    )
    # create database engine
    _engine = create_engine(db_url, echo=False)

    # invoke sqlalchemy metadata object
    Base.metadata.create_all(bind=_engine)

    return _engine


def db_session():
    """
    Create database session to allow transaction with the database tables
    """
    _engine = db_engine()
    _session = Session(bind=_engine)

    yield _session

    _session.close()  # close the session connection
    _engine.dispose()  # dispose the created engine and close sessin connection
