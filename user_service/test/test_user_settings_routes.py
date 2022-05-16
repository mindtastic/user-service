from http import client
from fastapi.testclient import TestClient
from user_service.app import app
from mongoengine import connect, disconnect
from unittest import TestCase
import json

#create test mongodb client
client = TestClient(app)

user_settings_data = {
  "userId": 1,
  "language": "de"
}

#testing class
class TestUserSettingsRoutes(TestCase):

    @classmethod
    def setUpClass(cls):
        disconnect()
        connect('mongoenginetest', host='mongomock://localhost/test_db')

    @classmethod
    def tearDownClass(cls):
        disconnect()
    
    #test create user settings endpoint
    def test_create_user_settings(self):
        response = client.post("user/1/settings", json.dumps(user_settings_data))
        assert response.status_code == 200

    #test get /user/{id} endpoint
    def test_get_user_settings_by_id(self):
        response = client.get("user/1/settings")
        assert response.status_code == 200
        assert response.json() == user_settings_data
    
    #test delete user settings endpoint
    def test_delete_user_settings(self):
        response = client.delete("user/1/settings")
        assert response.status_code == 200

    #test get /user/{id} endpoint to check if it's deleted
    #TODO: fails, needs to be fixed -> returns 200
    def test_get_user_settings_by_id_after_delete(self):
        response = client.get("user/1/settings")
        assert response.status_code == 404

    #test get for non existing user
    def test_get_user_settings_by_id_for_non_existing_user(self):
        response = client.get("user/3/settings")
        assert response.status_code == 404