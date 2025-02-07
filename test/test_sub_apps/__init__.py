#!/usr/bin/python3
"""
This module contains shared objects between package modules
"""
from fastapi.testclient import TestClient
from main.database.engine import db_session
from main.sub_apps.admin import admin
from test import TestingSessionLocal


# Override the dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Update the app to use the test database
admin.dependency_overrides[db_session] = override_get_db


# Create test client
client = TestClient(admin)
