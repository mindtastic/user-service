from http import client
import json
from fastapi.testclient import TestClient
from user_service.app import app


#create test mongodb client
client = TestClient(app)

user_settings_data = {
  "userId": 1,
  "language": "de",
}

#test create user settings endpoint
def test_create_user_settings():
    response = client.post("user/1/settings", json.dumps(user_settings_data))
    assert response.status_code == 200

#test creating duplicate user settings
def test_create_duplicate_user_settings():
    response = client.post("user/1/settings", json.dumps(user_settings_data))
    assert response.status_code == 409

#test get /user/{id} endpoint
def test_get_user_settings_by_id():
    response = client.get("user/1/settings")
    assert response.status_code == 200
    assert response.json() == user_settings_data

#test delete user settings endpoint
def test_delete_user_settings():
    response = client.delete("user/1/settings")
    assert response.status_code == 200

#test get user settings after deleting
def test_get_user_settings_after_deleting():
    response = client.get("user/1/settings")
    assert response.status_code == 404

#test create user settings for non existing user
def test_create_user_settings_for_non_existing_user():
    response = client.post("user/3/settings", json.dumps(user_settings_data))
    assert response.status_code == 404

#test get for non existing user
def test_get_user_settings_by_id_for_non_existing_user():
    response = client.get("user/3/settings")
    assert response.status_code == 404

#test delete for non existing user
def test_delete_user_settings_for_non_existing_user():
    response = client.delete("user/3/settings")
    assert response.status_code == 404
    