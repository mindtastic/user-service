from http import client
import json
from fastapi.testclient import TestClient
from user_service.app import app


#create test mongodb client
client = TestClient(app)

user_settings_data = {
  "user_id": "1b7c8e6c-f201-432e-8d5c-991b92a4a900",
  "language": "de",
}

USERDATA = {
    "user_id": "1b7c8e6c-f201-432e-8d5c-991b92a4a900",
    "username": "usersettingtest",
    "role": "admin",
}

def test_create_user():
    response = client.post("user/", json.dumps(USERDATA, default=str))
    assert response.status_code == 201

def test_create_user_settings():
    ''' test create user settings endpoint'''
    response = client.post("user/1b7c8e6c-f201-432e-8d5c-991b92a4a900/settings", json.dumps(user_settings_data))
    assert response.status_code == 200

#test get /user/{id} endpoint
def test_get_user_settings_by_id():
    response = client.get("user/1b7c8e6c-f201-432e-8d5c-991b92a4a900/settings")
    assert response.status_code == 200
    assert response.json() == {"language": "de"}

#test delete user settings endpoint
def test_delete_user_settings():
    response = client.delete("user/1b7c8e6c-f201-432e-8d5c-991b92a4a900/settings")
    assert response.status_code == 200

#test get user settings after deleting
def test_get_user_settings_after_deleting():
    response = client.get("user/1b7c8e6c-f201-432e-8d5c-991b92a4a900/settings")
    assert response.status_code == 404

#test create user settings for non existing user
def test_create_user_settings_for_non_existing_user():
    response = client.post("user/1b7c9e6c-f201-432e-8d5c-991b92a4a900/settings", json.dumps(user_settings_data))
    assert response.status_code == 404

#test get for non existing user
def test_get_user_settings_by_id_for_non_existing_user():
    response = client.get("user/1b7c9e6c-f201-432e-8d5c-991b92a4a900/settings")
    assert response.status_code == 404

#test delete for non existing user
def test_delete_user_settings_for_non_existing_user():
    response = client.delete("user/1b7c9e6c-f201-432e-8d5c-991b92a4a900/settings")
    assert response.status_code == 404

#delete test user
def test_delete_user():
    response = client.delete("user/1b7c8e6c-f201-432e-8d5c-991b92a4a900")
    assert response.status_code == 200