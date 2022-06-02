from http import client
import json
from fastapi.testclient import TestClient
from user_service.app import app

client = TestClient(app) #create test client

USERDATA = {
    "user_id": "123e4567-e89b-12d3-a456-426655440000",
    "username": "test",
    "role": "user",
}

INVALID_USERDATA = {
    "user_id": "123e4567-e89b-12d3-a456-426655440000",
    "username": "test",
    "role": "clown",
}

def test_get_all_users_before_creating():
    ''' test get users before creating '''
    response = client.get("user/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_user():
    '''test create user endpoint'''
    response = client.post("user/", json.dumps(USERDATA, default=str))
    assert response.status_code == 201

def test_create_user_with_invalid_data():
    '''test creating user with invalid data'''
    response = client.post("user/", json.dumps(INVALID_USERDATA, default=str))
    assert response.status_code == 422

def test_get_all_users():
    '''test returning all users'''
    response = client.get("user/")
    assert response.status_code == 200
    assert response.json() == [{
        "username": "test",
        "role": "user",
    }]

def test_get_not_existing_user_by_id():
    '''test returning a user by non-existing id'''
    response = client.get("user/123e4567-eaaa-12d3-a456-426655440000")
    assert response.status_code == 404

def test_get_user_by_id():
    '''test returning a user by id'''
    response = client.get("user/123e4567-e89b-12d3-a456-426655440000")
    assert response.status_code == 200

def test_update_user_with_valid_input():
    '''test updating a user record'''
    response = client.put(
        "user/123e4567-e89b-12d3-a456-426655440000",
        json.dumps({"username": "updated_test"})
    )
    assert response.status_code == 200

def test_update_user_with_invalid_input():
    '''test inserting invalid data'''
    response = client.put(
        "user/123e4567-e89b-12d3-a456-426655440000",
        json.dumps({"role": "clown"})
    )
    assert response.status_code == 422

def test_delete_user():
    '''test deleting user endpoint'''
    response = client.delete("user/123e4567-e89b-12d3-a456-426655440000")
    assert response.status_code == 200
