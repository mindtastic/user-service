from http import client
import json
from fastapi.testclient import TestClient
from user_service.app import app

USERDATA = {
    "username": "test",
    "role": "user",
}

INVALID_USERDATA = {
    "username": "test",
    "role": "clown",
}


with TestClient(app) as client:
    def test_get_all_users_before_creating():
        ''' test get users before creating '''
        response = client.get("users/admin")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_user():
        '''test create user endpoint'''
        response = client.post("users/admin", json.dumps(USERDATA, default=str), headers={"X-User-Id": "123e4567-e89b-12d3-a456-426655440000"})
        assert response.status_code == 201

    def test_create_user_with_invalid_data():
        '''test creating user with invalid data'''
        response = client.post("users/admin", json.dumps(INVALID_USERDATA, default=str), headers={"X-User-Id": "123e4567-e89b-12d3-a456-426655440000"})
        assert response.status_code == 422

    def test_get_all_users():
        '''test returning all users'''
        response = client.get("users/admin")
        assert response.status_code == 200
        assert response.json() == [{
            "username": "test",
            "role": "user",
        }]

    def test_get_not_existing_user_by_id():
        #test getting not existing user by id, should create the new user and return 201 created
        response = client.get("user", headers={"X-User-Id": "123e4567-eaaa-12d3-a456-426655440000"})
        assert response.status_code == 200

    def test_get_user_by_id():
        '''test returning a user by id'''
        # client.post(
        # "user/123e4567-e89b-12d3-a456-426655440000/settings",
        # json.dumps(USER_SETTINGS_DATA)
        # )
        response = client.get("user", headers={"X-User-Id": "123e4567-e89b-12d3-a456-426655440000"})
        assert response.status_code == 200

    def test_update_user_with_valid_input():
        '''test updating a user record'''
        response = client.put(
            "user",
            json.dumps({"username": "updated_test"}),
            headers={"X-User-Id": "123e4567-e89b-12d3-a456-426655440000"}
        )
        assert response.status_code == 200

    def test_update_user_with_invalid_input():
        '''test inserting invalid data'''
        response = client.put(
            "user",
            json.dumps({"role": "clown"}),
            headers={"X-User-Id": "123e4567-e89b-12d3-a456-426655440000"}
        )
        assert response.status_code == 422

    def test_delete_user():
        '''test deleting user endpoint'''
        response = client.delete("user", headers={"X-User-Id": "123e4567-e89b-12d3-a456-426655440000"})
        assert response.status_code == 200

    def test_deleted_user_settings():
        '''test whether deleted user's settings remain'''
        response = client.get("user/settings", headers={"X-User-Id": "123e4567-e89b-12d3-a456-426655440000"})
        assert response.status_code == 404
