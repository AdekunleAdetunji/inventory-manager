#!/usr/bin/python3
"""
This module contains the admin fastapi sub-application
"""
from fastapi import FastAPI
from main.database.models.admin import Admin
from main.sub_apps import *
from main.sub_apps.admin_routers import category
from main.validators.admin import AdminRequestValidator
from main.validators.admin import AdminResponseValidator

# create an instnce of the FastAPI application
admin = FastAPI()

# include the category router to category application
admin.include_router(category.router)


@admin.post(
    "/new-admin",
    response_model=AdminResponseValidator,
    tags=["WRITE"],
)
def create_admin(
    request: AdminRequestValidator, session: Session = Depends(db_session)
):
    """operation to create new admin in the admin database"""
    # create admin object
    admin_obj = Admin(**request.model_dump())
    try:
        # add admin_obj to database session
        session.add(admin_obj)
        # commit the session to the database
        session.commit()
    except exc.IntegrityError as IntegrityError:
        # rollback the session
        session.rollback()
        # pass error_obj to integrity_error_handler and raise the correct error
        raise sqlalchemy_err_utils.integrity_error_handler(IntegrityError)

    return admin_obj
