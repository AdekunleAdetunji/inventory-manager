#!/usr/bin/python3
"""
This module contains the category router and path operations for carrying
out CRUD operations on the Category database table
"""
from fastapi import APIRouter
from fastapi import Depends
from main.database.engine import db_session
from main.database.models.category import Category
from main.validators.category import CategoryRequestValidator
from main.validators.category import CategoryResponseValidator
from main.utils import http_exc
from main.utils import sqlalchemy_err_utils
from sqlalchemy import exc
from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID

# instantiate the category APIRouter
router = APIRouter()


@router.get(
    "/categories",
    response_model=list[CategoryResponseValidator],
    tags=["READ"],
)
async def all_categories(session: Session = Depends(db_session)):
    """get all records in the inventory-db database category table"""
    # query the database for all category objects
    categories = session.scalars(select(Category)).all()
    return categories


@router.get(
    "/category_by_id/{identifier}",
    response_model=CategoryResponseValidator,
    tags=["READ"],
)
async def get_category_by_id(
    identifier: UUID, session: Session = Depends(db_session)
):
    """
    Get a given record from the inventory-db category table using category_id filter
    """
    # create select statement object
    stmt = select(Category).where(Category.id == identifier)
    # query the database for a given category using its name
    cat_obj = session.scalars(stmt).first()
    # raise HTTPException if category object not found
    if not cat_obj:
        # rollback the session
        session.rollback()
        raise http_exc.not_found(Category, identifier)

    return cat_obj


@router.get(
    "/category_by_name/{identifier}",
    response_model=CategoryResponseValidator,
    tags=["READ"],
)
async def get_category_by_name(
    identifier: str, session: Session = Depends(db_session)
):
    """
    Get a given record from the inventory-db category table using category_id filter
    """
    # create select statement object
    stmt = select(Category).where(Category.name == identifier)
    # query the database for a given category using its name
    cat_obj = session.scalars(stmt).first()
    # raise HTTPException if category object not found
    if not cat_obj:
        # rollback the session
        session.rollback()
        raise http_exc.not_found(Category, identifier)

    return cat_obj


@router.post(
    "/category", response_model=CategoryResponseValidator, tags=["WRITE"]
)
async def create_category(
    request: CategoryRequestValidator, session: Session = Depends(db_session)
):
    """Insert a new category into the Category table"""
    # create Category object
    cat_obj = Category(**request.model_dump())
    try:
        # add the cat_obj to the session object
        session.add(cat_obj)
        # commit the changes to the database
        session.commit()
    except exc.IntegrityError as IntegrityError:
        # rollback the session
        session.rollback()
        # pass error_obj to integrity_error_handler and raise the correct error
        raise sqlalchemy_err_utils.integrity_error_handler(IntegrityError)

    return cat_obj
