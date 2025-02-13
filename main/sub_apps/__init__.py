#!/usr/bin/python3
"""
This module contains shared imports and object between the admin_router modules
"""
import jwt
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from main.database.models.admin import Admin
from main.validators.token import TokenData
from sqlalchemy import select
from sqlalchemy.orm import Session


# get the public and private keys used to generate the toke
with open("private_key.pem", "r") as file_obj:
    PRIVATE_KEY = file_obj.read()
with open("public_key.pem", "r") as file_obj:
    PUBLIC_KEY = file_obj.read()

# set the algorithm used to encode and decode jwt
ALGORITHM = "RS256"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> dict:
    """
    create jwt with the data supplied

    parameters
    ----------
    data: dict
        data to be used to sign token

    return: dict
        jwt
    """
    to_encode = data.copy()
    # compute and set token expiration time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    # update the to_encode dictionary with the expire datetime object
    to_encode.update({"exp": expire})
    # encode the data
    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def validate_token(
    token: str,
    session: Session,
):
    """
    authenticate the supplied token

    parameters
    ----------
    token: str
        token supplied with request

    return: TokenData
    """
    # create a credential error exception object
    cred_exc = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credential",
    )
    try:
        payload: dict = jwt.decode(token, PUBLIC_KEY, [ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise cred_exc
        # check if username still exists in database
        stmt = select(Admin).where(Admin.email == username)
        admin_obj = session.scalars(stmt).first()
        if not admin_obj:
            raise cred_exc
    except InvalidTokenError as err_obj:
        raise cred_exc
    return TokenData(email=username)
