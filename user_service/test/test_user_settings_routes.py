from http import client
import json
import pytest
from fastapi.testclient import TestClient
from user_service.app import app
import user_service.database as database
import mongomock

#create test mongodb client

with database.ClientManager() as db_client:
    db_client = mongomock.MongoClient()
    logging.info("Connected to mongomock database")    

user_settings_data = {
  "language": "de",
}

USERDATA = {
    "username": "usersettingtest",
    "role": "admin",
}

with TestClient(app) as client:
    def test_create_user():
        response = client.post("users/admin", json.dumps(USERDATA, default=str), headers={"X-User-Id": "1b7c8e6c-f201-432e-8d5c-991b92a4a900"})
        assert response.status_code == 201

    def test_create_user_settings():
        ''' test create user settings endpoint'''
        response = client.post("user/settings", json.dumps(user_settings_data), headers={"X-User-Id": "1b7c8e6c-f201-432e-8d5c-991b92a4a900"})
        assert response.status_code == 200

    #test get /user/{id} endpoint
    def test_get_user_settings_by_id():
        response = client.get("user/settings", headers={"X-User-Id": "1b7c8e6c-f201-432e-8d5c-991b92a4a900"})
        assert response.status_code == 200
        assert response.json() == {"language": "de"}

    #test delete user settings endpoint
    def test_delete_user_settings():
        response = client.delete("user/settings", headers={"X-User-Id": "1b7c8e6c-f201-432e-8d5c-991b92a4a900"})
        assert response.status_code == 200

    #test get user settings after deleting
    def test_get_user_settings_after_deleting():
        response = client.get("user/settings", headers={"X-User-Id": "1b7c8e6c-f201-432e-8d5c-991b92a4a900"})
        assert response.status_code == 404

    #test create user settings for non existing user
    def test_create_user_settings_for_non_existing_user():
        response = client.post("user/settings", json.dumps(user_settings_data), headers={"X-User-Id": "a8ce4c84-f87b-11ec-b939-0242ac120002"})
        assert response.status_code == 404

    #test get for non existing user
    def test_get_user_settings_by_id_for_non_existing_user():
        response = client.get("user/settings", headers={"X-User-Id": "a8ce4c84-f87b-11ec-b939-0242ac120002"})
        assert response.status_code == 404

    #test delete for non existing user
    def test_delete_user_settings_for_non_existing_user():
        response = client.delete("user/settings", headers={"X-User-Id": "a8ce4c84-f87b-11ec-b939-0242ac120002"})
        assert response.status_code == 404

    #delete test user
    def test_delete_user():
        response = client.delete("user", headers={"X-User-Id": "1b7c8e6c-f201-432e-8d5c-991b92a4a900"})
        assert response.status_code == 200
