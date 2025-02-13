#!/usr/bin/python3
"""
This module contains testsuites for operations defined in the sub_application
admin module
"""
from test.test_sub_apps import client
from test.test_sub_apps import token
from uuid import uuid4


def test_create_admin_success(admin_kwargs):
    """
    test create_admin operation creates successfully with the right request body
    """
    response = client.post("/new-admin", json=admin_kwargs)
    assert response.status_code == 201


def test_create_admin_fail_no_email(admin_kwargs):
    """
    test create_admin fails and returns a status code of 422 when called with
    a json without an email field
    """
    # assign None value to the admin _kwargs email key
    admin_kwargs["email"] = None
    response = client.post("/new-admin", json=admin_kwargs)
    assert response.status_code == 422


def test_create_admin_fail_no_password(admin_kwargs):
    """
    test create_admin fails and returns a status code of 422 when called with
    a json without a password field
    """
    # assign None value to the admin _kwargs password key
    admin_kwargs["password"] = None
    response = client.post("/new-admin", json=admin_kwargs)
    assert response.status_code == 422


def test_create_admin_fail_no_first_name(admin_kwargs):
    """
    test create_admin fails and returns a status code of 422 when called with
    a json without a first_name field
    """
    # assign None value to the admin _kwargs first_name key
    admin_kwargs["first_name"] = None
    response = client.post("/new-admin", json=admin_kwargs)
    assert response.status_code == 422


def test_create_admin_fail_no_last_name(admin_kwargs):
    """
    test create_admin fails and returns a status code of 422 when called with
    a json without a last_name field
    """
    # assign None value to the admin _kwargs last_name key
    admin_kwargs["last_name"] = None
    response = client.post("/new-admin", json=admin_kwargs)
    assert response.status_code == 422


def test_create_admin_fail_inv_email(admin_kwargs):
    """
    test create_admin fails and returns a status code of 422 when a json with
    an invalid email is provided
    """
    # assign an invalid email string to the admin_kwargs email key
    admin_kwargs["email"] = "admin email"
    response = client.post("/new-admin", json=admin_kwargs)
    assert response.status_code == 422


def test_create_admin_fail_inv_password(admin_kwargs):
    """
    test create_admin fails and returns a status code of 422 when a json with
    an invalid password is provided
    """
    # assign an invalid value to the admin_kwargs password key
    admin_kwargs["password"] = 23
    response = client.post("/new-admin", json=admin_kwargs)
    assert response.status_code == 422


def test_create_admin_fail_inv_first_name(admin_kwargs):
    """
    test create_admin fails and returns a status code of 422 when a json with
    an invalid first_name is provided
    """
    # assign an invalid value to the admin_kwargs first_name key
    admin_kwargs["first_name"] = list("123")
    response = client.post("/new-admin", json=admin_kwargs)
    assert response.status_code == 422


def test_create_admin_fail_inv_last_name(admin_kwargs):
    """
    test create_admin fails and returns a status code of 422 when a json with
    an invalid last_name is provided
    """
    # assign an invalid value to the admin_kwargs last_name key
    admin_kwargs["last_name"] = {"a": "b"}
    response = client.post("/new-admin", json=admin_kwargs)
    assert response.status_code == 422


def test_create_admin_fail_column_conflict(admin_kwargs):
    """
    test create_admin fails and returns the 409 status code as a result of
    conflict
    """
    response_1 = client.post("/new-admin", json=admin_kwargs)
    assert response_1.status_code == 201
    response_2 = client.post("/new-admin", json=admin_kwargs)
    assert response_2.status_code == 409


def test_get_admin_info_success(admin_kwargs):
    """
    test that get_admin_info operation returns a 200 success status code
    """
    # register a new admin
    response = client.post(
        "/new-admin",
        json=admin_kwargs,
    )
    assert response.status_code == 201
    # login to obtain access token for new admin
    login_response = client.post("/token", data=admin_kwargs)
    assert login_response.status_code == 200
    # extract access_token from response
    token = login_response.json()["access_token"]
    # verify that access_token works
    response = client.get(
        "/admin-info",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200, response.json()


def test_get_admin_info_fail(admin_kwargs):
    """
    test that get_admin_info operation fails when no admin is logged in
    """
    response = client.get("/admin-info")
    assert response.status_code == 401


def test_login_for_access_token_success(admin_kwargs):
    """
    test that the login_for_access_token operator works properly with the right
    username and password provided
    """
    # register a new admin to the database
    response = client.post("/new-admin", json=admin_kwargs)
    assert response.status_code == 201
    # login to the admin account to obtain token
    response = client.post("/token", data=admin_kwargs)
    assert (
        response.status_code == 200
        and response.json()
        and response.json()["access_token"]
        and response.json()["token_type"]
    )


def test_login_for_access_token_fail_inv_username(admin_kwargs):
    """
    test that login_for_access_token operator fails when supplied invalid
    username
    """
    # register a new admin to the database
    response = client.post("/new-admin", json=admin_kwargs)
    assert response.status_code == 201
    # change the admin_kwargs username value
    admin_kwargs["username"] = "user@example.com"
    # login to the admin account to obtain token
    response = client.post("/token", data=admin_kwargs)
    assert (
        response.status_code == 401
        and response.json()["detail"] == "Incorrect Username and/or Password"
    )


def test_login_for_access_token_fail_inv_password(admin_kwargs):
    """
    test that login_for_access_token operator fails when supplied invalid
    password
    """
    # register a new admin to the database
    response = client.post("/new-admin", json=admin_kwargs)
    assert response.status_code == 201
    # change the admin_kwargs password value
    admin_kwargs["username"] = "user@example.com"
    # login to the admin account to obtain token
    response = client.post("/token", data=admin_kwargs)
    assert (
        response.status_code == 401
        and response.json()["detail"] == "Incorrect Username and/or Password"
    )


def test_login_for_access_token_fail_none_data(admin_kwargs):
    """
    test that login_for_access_token operator fails when supplied data with
    username and password assigned a None value
    """
    # register a new admin to the database
    response = client.post("/new-admin", json=admin_kwargs)
    assert response.status_code == 201
    # set username and password field to None values
    admin_kwargs["username"] = None
    admin_kwargs["password"] = None
    # login to the admin account to obtain token
    response = client.post("/token", data=admin_kwargs)
    assert (
        response.status_code == 401
        and response.json()["detail"] == "Incorrect Username and/or Password"
    )


def test_login_for_access_token_fail_no_username(admin_kwargs):
    """
    test that login_for_access_token operator fails when supplied data with no
    username field value
    """
    # register a new admin to the database
    response = client.post("/new-admin", json=admin_kwargs)
    assert response.status_code == 201
    # delete the username admin_kwargs value
    admin_kwargs.pop("username")
    # login to the admin account to obtain token
    response = client.post("/token", data=admin_kwargs)
    assert response.status_code == 422


def test_login_for_access_token_fail_no_password(admin_kwargs):
    """
    test that login_for_access_token operator fails when supplied data with no
    password field value
    """
    # register a new admin to the database
    response = client.post("/new-admin", json=admin_kwargs)
    assert response.status_code == 201
    # delete the username admin_kwargs value
    admin_kwargs.pop("password")
    # login to the admin account to obtain token
    response = client.post("/token", data=admin_kwargs)
    assert response.status_code == 422


def test_update_admin_info_success(token, admin_kwargs):
    """
    test that update_admin_info operator successfully updates and existing
    with new admin info provided
    """
    response = client.get(
        "/admin-info",
        headers={"Authorization": f"Bearer {token}"},
    )
    admin_obj = response.json()
    assert (
        response.status_code == 200
        and admin_obj["first_name"] == "admin"
        and admin_obj["last_name"] == "admin"
    )
    # update the admin_kwargs first_name and last_name values
    admin_kwargs["first_name"] = "first_name"
    admin_kwargs["last_name"] = "last_name"
    # update the admin object in the database
    response = client.put(
        "/update-info",
        json=admin_kwargs,
        headers={"Authorization": f"Bearer {token}"},
    )
    updated_admin_obj = response.json()
    assert (
        response.status_code == 200
        and updated_admin_obj["id"] == admin_obj["id"]
        and updated_admin_obj["first_name"] != admin_obj["first_name"]
        and updated_admin_obj["last_name"] != admin_obj["last_name"]
    )


def test_update_admin_info_success_no_first_name(token, admin_kwargs):
    """
    test that update_admin_info operators return success status code when
    json data has no first_name argument
    """
    response = client.get(
        "/admin-info",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    admin_obj = response.json()
    # delete the first_name key from admin_kwargs
    del admin_kwargs["first_name"]
    # update the admin_kwargs last_name value
    admin_kwargs["last_name"] = "last_name"
    # update the admin object in the database
    response = client.put(
        "/update-info",
        json=admin_kwargs,
        headers={"Authorization": f"Bearer {token}"},
    )
    updated_admin_obj = response.json()
    assert (
        response.status_code == 200
        and updated_admin_obj["id"] == admin_obj["id"]
        and updated_admin_obj["first_name"] == admin_obj["first_name"]
        and updated_admin_obj["last_name"] != admin_obj["last_name"]
    )


def test_update_admin_info_success_no_last_name(token, admin_kwargs):
    """
    test that update_admin_info operators return success status code when
    json data has no last_name argument
    """
    response = client.get(
        "/admin-info",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    admin_obj = response.json()
    # delete the last_name key from admin_kwargs
    del admin_kwargs["first_name"]
    # update the admin_kwargs first_name value
    admin_kwargs["first_name"] = "first_name"
    # update the admin object in the database
    response = client.put(
        "/update-info",
        json=admin_kwargs,
        headers={"Authorization": f"Bearer {token}"},
    )
    updated_admin_obj = response.json()
    assert (
        response.status_code == 200
        and updated_admin_obj["id"] == admin_obj["id"]
        and updated_admin_obj["first_name"] != admin_obj["first_name"]
        and updated_admin_obj["last_name"] == admin_obj["last_name"]
    )


def test_update_admin_info_fail_inv_first_name(token, admin_kwargs):
    """
    test that update_admin_info operator fails due to invalid first_name field
    data type
    """
    # update the admin_kwargs first_name key to hold an integer value
    admin_kwargs["first_name"] = 23
    # update the admin object in the database
    response = client.put(
        "/update-info",
        json=admin_kwargs,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422


def test_update_admin_info_fail_inv_last_name(token, admin_kwargs):
    """
    test that update_admin_info operator fails due to invalid last_name field
    data type
    """
    # update the admin_kwargs last_name key to hold an empty list
    admin_kwargs["last_name"] = []
    # update the admin object in the database
    response = client.put(
        "/update-info",
        json=admin_kwargs,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422


def test_change_password_success(token, admin_kwargs):
    """
    test that the change_password operator works properly when the right json
    data is supplied
    """
    # create the new_password and old_password json to be sent with the request
    json_data = {
        "new_password": "new_password",
        "old_password": admin_kwargs["password"],
    }
    # change the password for the admin logged
    response = client.put(
        "/change-password",
        json=json_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    # verify that the password change is effected in the database by logging in
    # with new password but first with old password
    response = client.post("/token", data=admin_kwargs)
    assert response.status_code == 401
    admin_kwargs["password"] = json_data["new_password"]
    response = client.post("/token", data=admin_kwargs)
    assert response.status_code == 200


def test_change_password_fail_inv_old_password(token):
    """
    test that change_password operator fails when an invalid old password is
    supplied
    """
    # create the new_password and old_password json to be sent with the request
    json_data = {
        "new_password": "new_password",
        "old_password": "old_password",
    }
    # change the password of the signed in admin
    response = client.put(
        "/change-password",
        json=json_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401


def test_change_password_fail_no_new_password(token, admin_kwargs):
    """
    test that change_password operator fails when there is no new password
    field is present in the json data sent with the request
    """
    # change the password of the signed in admin
    response = client.put(
        "/change-password",
        json={"old_password": admin_kwargs["password"]},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422


def test_change_password_fail_no_old_password(token):
    """
    test that change_password operator fails when there is no new password
    field is present in the json data sent with the request
    """
    # change the password of the signed in admin
    response = client.put(
        "/change-password",
        json={"new_password": "new_password"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422


def test_change_password_fail_inv_new_password(token, admin_kwargs):
    """
    test that change_password operator fails when the new_password field in the
    json data sent with the request has an invalid value
    """
    # create the new_password and old_password json to be sent with the request
    json_data = {
        "new_password": "new_password",
        "old_password": 123,
    }
    # change the password of the signed in admin
    response = client.put(
        "/change-password",
        json=json_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422


def test_change_password_fail_inv_new_password(token, admin_kwargs):
    """
    test that change_password operator fails when the old_password field in the
    json data sent with the request has an invalid value
    """
    # create the new_password and old_password json to be sent with the request
    json_data = {
        "new_password": list("1223"),
        "old_password": admin_kwargs["password"],
    }
    # change the password of the signed in admin
    response = client.put(
        "/change-password",
        json=json_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422


def test_delete_admin_success(token, admin_kwargs):
    """
    test that delete_admin operator succeeds when a valid token is provided
    """
    delete_response = client.delete(
        "/delete-admin",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert delete_response.status_code == 200
    # attempt to login into the admin again
    login_response = client.post("/token", data=admin_kwargs)
    assert login_response.status_code == 401


def test_delete_admin_fail_no_token():
    """
    test that delete_admin operator fails when no token is sent with the
    request
    """
    delete_response = client.delete("/delete-admin")
    assert delete_response.status_code == 401
