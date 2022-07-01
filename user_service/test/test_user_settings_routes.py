from http import client
import json
from fastapi.testclient import TestClient
from user_service.app import app
from mongomock_motor import AsyncMongoMockClient

from user_service.routes.dependencies import  _get_settings_collection, _get_users_collection

#create test mongodb client

USERSETTINGSDATA = {
  "language": "de",
}

USERDATA = {
    "username": "usersettingtest",
    "role": "admin",
}

with TestClient(app) as client:

    async def override_mongodb_users_collection_dependency():
        override_users_collection = AsyncMongoMockClient()['users']['users_collection']
        return override_users_collection

    async def override_mongodb_user_settings_collection_dependency():
        override_settings_collection = AsyncMongoMockClient()['users']['user_settings_collection']
        return override_settings_collection

    #override mongodb dependency
    app.dependency_overrides[_get_users_collection] = override_mongodb_users_collection_dependency
    app.dependency_overrides[_get_settings_collection] = override_mongodb_user_settings_collection_dependency 

    def test_create_user():
        response = client.post("users/admin", json.dumps(USERDATA, default=str), headers={"X-User-Id": "1b7c8e6c-f201-432e-8d5c-991b92a4a900"})
        assert response.status_code == 201

    def test_create_user_settings():
        ''' test create user settings endpoint'''
        response = client.post("user/settings", json.dumps(USERSETTINGSDATA), headers={"X-User-Id": "1b7c8e6c-f201-432e-8d5c-991b92a4a900"})
        assert response.status_code == 200

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
        response = client.post("user/settings", json.dumps(USERSETTINGSDATA), headers={"X-User-Id": "a8ce4c84-f87b-11ec-b939-0242ac120002"})
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

    app.dependency_overrides = {}
