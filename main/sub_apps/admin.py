#!/usr/bin/python3
"""
This module contains the admin fastapi sub-application
"""
from fastapi import FastAPI
from main.sub_apps.admin_routers import category

# create an instnce of the FastAPI application
admin = FastAPI()

# include the category router to category application
admin.include_router(category.router)
