#!/usr/bin/python3
"""
This module contains shared imports and object between the admin_router modules
"""
from fastapi import Depends
from main.database.engine import db_session
from main.utils import http_exc
from main.utils import sqlalchemy_err_utils
from sqlalchemy import exc
from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID
