#!/usr/bin/python3
"""
This module contains user defined exception function that returns FastAPI
HTTPException depending on error type
"""
from fastapi import status
from fastapi import HTTPException


def not_found(model, identifier: str):
    """
    404_NOT_FOUND exception

    parameters
    ----------
    model_name: str
        The sqlalchemy model queried
    identifier: str
        The identifier used as query filter

    return: HTTPException
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{model.__name__} with identifier {identifier} not found",
    )


def conflict(sql_exc: Exception):
    """
    CONFLICT error raised for unsuccessful session commit

    parameters
    ----------
    sql_exc:
        sqlalchemy exception raised

    return: HTTPException
    """
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=str(sql_exc),
    )


def bad_request(sql_exc: Exception):
    """
    400_BAD_REQUEST error raised when the data sent with a request is invalid

    parameters
    ----------
    sql_exc:
        sqlalchemy error that caused this exception

    return: HTTPException
    """
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail=str(sql_exc)
    )
