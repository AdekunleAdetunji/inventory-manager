#!/usr/bin/python3
"""
This module contains the main fastapi applications
"""
from fastapi import FastAPI
from main.admin import admin


# assign an instance of a FastAPI class to main variable
main = FastAPI()


main.mount("/admin", admin)
