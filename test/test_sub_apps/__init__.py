#!/usr/bin/python3
"""
This module contains shared objects between test_sub_apps package modules
"""
import pytest
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


@pytest.fixture()
def token(admin_kwargs):
    """fixture to create new admin and yield the login response the new admin"""
    # register a new admin to the database
    response = client.post("/new-admin", json=admin_kwargs)
    assert response.status_code == 201
    # login to obtain access token for new admin
    login_response = client.post("/token", data=admin_kwargs)
    assert login_response.status_code == 200

    # yield token from login response
    yield login_response.json()["access_token"]
