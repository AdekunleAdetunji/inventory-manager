#!/usr/bin/python3
"""
This module contains utility functions that handles raising of http exceptions
when sqlalchemy exception is encountered
"""
from main.utils import http_exc
from psycopg2 import errors
from sqlalchemy import exc


def integrity_error_handler(sqlalchemy_err_obj: exc.IntegrityError):
    """
    function to handle sqlalchemy integrity error when encountered

    parameters
    ----------
    err_obj: IntegrityError
        Integrity error object encounted

    return: HTTPException
        user defined HTTPException
    """
    # check that
    if isinstance(sqlalchemy_err_obj.orig, errors.UniqueViolation):
        return http_exc.conflict(sqlalchemy_err_obj.orig)
    else:
        return http_exc.conflict(sqlalchemy_err_obj)


def data_error_handler(sqlalchemy_err_obj: exc.DataError):
    """
    function to handle sqlalchemy data error when encountered

    parameters
    ----------
    err_obj: DataError
        Integrity error object encounted

    return: HTTPException
        user defined HTTPException
    """
    if isinstance(sqlalchemy_err_obj.orig, errors.InvalidTextRepresentation):
        return http_exc.bad_request(sqlalchemy_err_obj.orig)
    else:
        return http_exc.bad_request(sqlalchemy_err_obj)
