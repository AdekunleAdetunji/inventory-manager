#!/usr/bin/python3
"""
Admin FastAPI Sub-application

This module defines the FastAPI sub-application for admin-related operations.
It includes routes for creating admins, authenticating admins, updating admin
information, and changing admin passwords. The application also handles
token-based authentication for secure access.

Modules and Packages:
- FastAPI: Main framework
- SQLAlchemy: Database session and query handling
- Validators: Request and response validation for admin operations
- Security: OAuth2 for authentication

Token expiration duration: 30 minutes
"""
from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from main.database.engine import db_session
from main.database.models.admin import Admin
from main.sub_apps import create_token, oauth2_scheme, validate_token
from main.sub_apps.admin_routers import category
from main.utils import sqlalchemy_err_utils
from main.validators.admin import (
    AdminRequestValidator,
    AdminResponseValidator,
    NewAdminPassRequestValidator,
    PutAdminRequestValidator,
)
from main.validators.token import Token
from sqlalchemy import exc, select, update
from sqlalchemy.orm import Session
from typing import Annotated

# Create an instance of the FastAPI sub-application
admin = FastAPI(title="Admin Sub-Application", version="1.0")

# Token expiration duration (30 minutes)
access_token_expires = timedelta(minutes=30)


@admin.post(
    "/new-admin",
    status_code=status.HTTP_201_CREATED,
    response_model=AdminResponseValidator,
    tags=["ADMIN"],
    description="""
    **Create New Admin**

    This endpoint allows the creation of a new admin in the database.  
    The request body should contain all required admin details such as name, \
email, and password. Upon successful creation, the new admin's details will be returned.
""",
)
def create_admin(
    request: AdminRequestValidator,
    session: Session = Depends(db_session),
):
    """
    Create a new admin account.

    This endpoint allows you to create a new admin account by providing the
    necessary details in the request body. If the email already exists, an
    error will be raised.

    **Parameters:**
    - `request`: AdminRequestValidator
        Contains admin details (name, email,password).
    - `session`: Session
        Database session dependency.

    **Returns:**
    - `AdminResponseValidator`: The created admin object.

    **Raises:**
    - `IntegrityError`: If the admin email already exists in the database.
    """
    # Create an admin object from the request data
    admin_obj = Admin(**request.model_dump())
    try:
        # Add the admin object to the database session
        session.add(admin_obj)
        # Commit the session to persist changes in the database
        session.commit()
    except exc.IntegrityError as IntegrityError:
        # Roll back the session in case of an IntegrityError
        # (e.g., duplicate email)
        session.rollback()
        raise sqlalchemy_err_utils.integrity_error_handler(IntegrityError)

    # Return the newly created admin object
    return admin_obj


@admin.post(
    "/token",
    response_model=Token,
    tags=["ADMIN"],
    description="""
    **Generate Authentication Token**
    
    This endpoint generates an access token for admin authentication.  
    The token is required to access other protected routes. It is valid for \
30 minutes and must be passed as a Bearer token in subsequent requests.
""",
)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(db_session),
):
    """
    Generate an authentication token for an admin.

    This endpoint authenticates an admin using their email and password, and
    returns a token for future requests.

    **Parameters:**
    - `form_data`: OAuth2PasswordRequestForm
        Contains `username` (email) and `password`.
    - `session`: Session
        Database session dependency.

    **Returns:**
    - `Token`: Access token for authentication.

    **Raises:**
    - `HTTPException`: If the email or password is incorrect.
    """
    # Query the admin table
    stmt = select(Admin).where(Admin.email == form_data.username)
    admin_obj = session.scalars(stmt).first()
    if not admin_obj or admin_obj.password != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Username and/or Password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "access_token": create_token(
            {"sub": admin_obj.email},
            access_token_expires,
        )
    }


@admin.get(
    "/admin-info",
    response_model=AdminResponseValidator,
    tags=["ADMIN"],
    description="""
    **Get Admin Info**

    This endpoint retrieves the details of the authenticated admin using the \
provided token.
    It returns the admin's full profile, including name and email.
""",
)
def get_admin_info(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(db_session),
):
    """
    Retrieve admin information.

    This endpoint fetches admin details using a valid authentication token.

    **Parameters:**
    - `token`: str
        Bearer token for authentication.
    - `session`: Session
        Database session dependency.

    **Returns:**
    - `AdminResponseValidator`: The admin object.
    """
    # fetch admin email from the token
    token_data = validate_token(token, session)
    # fetch admin object from database
    stmt = select(Admin).where(Admin.email == token_data.email)
    admin_obj = session.scalars(stmt).first()
    return admin_obj


@admin.put(
    "/update-info",
    response_model=AdminResponseValidator,
    tags=["ADMIN"],
    description="""
    **Update Admin Info**
    
    This endpoint updates the authenticated admin’s information.  
    You can update one or multiple fields such as name, contact information,\
and other details.  
    Only non-null fields from the request body will be updated.
""",
)
def update_admin_info(
    request: PutAdminRequestValidator,
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(db_session),
):
    """
    Update admin information.

    This endpoint allows an admin to update their information, such as name
    and other details. The request body should contain the fields to update.

    **Parameters:**
    - `request`: PutAdminRequestValidator
        Contains fields to update.
    - `token`: str
        Bearer token for authentication.
    - `session`: Session
        Database session dependency.

    **Returns:**
    - `AdminResponseValidator`: The updated admin object.
    """
    # validate and fetch admin email from token
    token_data = validate_token(token, session)
    admin_email = token_data.email
    # get update data
    data = {key: value for key, value in request.model_dump().items() if value}
    # create the update statement
    stmt = (
        update(Admin)
        .where(Admin.email == admin_email)
        .values(**data)
        .returning(Admin)
    )
    # execute the update statement
    admin_obj = session.scalars(stmt).first()
    session.commit()
    return admin_obj


@admin.put(
    "/change-password",
    response_model=AdminResponseValidator,
    tags=["ADMIN"],
    description="""
    **Change Admin Password**

    This endpoint allows the authenticated admin to change their password.  
    The request must include the current password and the new password. If \
the current password does not match the stored password, an error will be \
raised.
""",
)
def change_password(
    request: NewAdminPassRequestValidator,
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(db_session),
):
    """
    Change admin password.

    This endpoint allows an admin to change their password by providing the
    old password and a new one.

    **Parameters:**
    - `request`: NewAdminPassRequestValidator
        Contains `old_password` and `new_password`.
    - `token`: str
        Bearer token for authentication.
    - `session`: Session
        Database session dependency.

    **Returns:**
    - `AdminResponseValidator`: The updated admin object.

    **Raises:**
    - `HTTPException`: If the old password is incorrect.
    """
    # validate the supplied token
    token_data = validate_token(token, session)
    # get admin email from token_data
    admin_email = token_data.email
    # obtain the admin object in the admin table
    admin_obj = session.scalars(
        select(Admin).where(Admin.email == admin_email),
    ).first()
    # check that the new password is same as the old one
    if not admin_obj or admin_obj.password != request.old_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Old password is incorrect",
        )
    # update the admin_obj password field with new password
    admin_obj.password = request.new_password
    # commit the changes to the database
    session.commit()

    return admin_obj


@admin.delete(
    "/delete-admin",
    tags=["ADMIN"],
    description="""
    **Delete Admin Account**

    This endpoint deletes the authenticated admin account from the database.  
    Once deleted, the admin’s account cannot be recovered.  
    A valid token is required for authentication.
""",
)
def delete_admin(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(db_session),
):
    """
    Delete an admin account.

    This endpoint deletes the admin account associated with the provided
    authentication token. The admin is permanently removed from the database.

    **Parameters:**
    - `token`: str
        Bearer token for authentication and identification of the admin to be
        deleted.
    - `session`: Session
        Database session used for querying and deleting the admin object.

    **Returns:**
    - `JSONResponse`: A success message indicating the admin account was
        deleted.

    **Raises:**
    - `HTTPException`: 401 Unauthorized - If the token is invalid or expired.
    - `HTTPException`: 404 Not Found - If the admin does not exist in the
        database.
    """
    # fetch admin email from the token
    token_data = validate_token(token, session)
    # fetch admin object from database
    stmt = select(Admin).where(Admin.email == token_data.email)
    admin_obj = session.scalars(stmt).first()

    # delete admin_obj from table
    session.delete(admin_obj)
    session.commit()

    return JSONResponse(content={"detail": "success"})


# include the category router
admin.include_router(category.router)
