#!/usr/bin/python3
"""
This module contains the main fastapi applications
"""
from fastapi import FastAPI
from main.sub_apps.admin import admin


# assign an instance of a FastAPI class to main variable
app = FastAPI()


# mount the admin application of the main application
app.mount("/admin", admin)
