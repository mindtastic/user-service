from http import client
import json
from fastapi.testclient import TestClient
from user_service.app import app

client = TestClient(app) #create test client

USERDATA = {
    "userId": "1",
    "username": "test",
    "email": "test@test.com",
    "role": "user",
}

INCOMPLETE_DATA = {
    "userId": "1",
    "email": "test@test.com",
    "role": "user",
}

INVALID_USERDATA = {
    "userId": "1",
    "username": "test",
    "email": "test@test.com",
    "role": "clown",
}

# test create user endpoint
def test_create_user():
    response = client.post("user/", json.dumps(USERDATA, default=str))
    assert response.status_code == 200

def test_create_user_with_incomplete_data():
    response = client.post("user/", json.dumps(INCOMPLETE_DATA, default=str))
    assert response.status_code == 422

def test_create_user_with_invalid_data():
    response = client.post("user/", json.dumps(INVALID_USERDATA, default=str))
    assert response.status_code == 422

# # test get /user endpoint
# TODO fix tests once test db is used
# def test_get_all_users():
#     response = client.get("user/")
#     assert response.status_code == 200
#     assert response.json() == [USERDATA]

# test get /user/{id} enpoint
def test_get_not_existing_user_by_id():
    response = client.get("user/0123456789")
    assert response.status_code == 404

def test_get_user_by_id():
    response = client.get("user/1")
    assert response.status_code == 200

# test put /user/{id} endpoint
def test_update_user_with_valid_input():
    response = client.put("user/1", json.dumps({"username": "updated_test"}))
    assert response.status_code == 200

def test_update_user_with_invalid_input():
    response = client.put("user/1", json.dumps({"role": "clown"}))
    assert response.status_code == 422

def test_delete_user():
    response = client.delete("user/1")
    assert response.status_code == 200
