from http import client
from fastapi.testclient import TestClient
from user_service.app import app
import json
from datetime import datetime

client = TestClient(app) #create test client

user_data = {"id": "1", "username": "test", "email": "test@test.com", "password": "testing", "role": "user", "lang": "de"}

# test create user endpoint
def test_create_user():
  response = client.post("user/", json.dumps(user_data))
  assert response.status_code == 200
  assert response.json()["email"] == "test@test.com"
  assert response.json()["lang"] == "de"


# test get /users endpoint
def test_get_all_users():
  response = client.get("user/")
  assert response.status_code == 200
  assert response.json() == [{"id": "1", "username": "test", "email": "test@test.com", "role": "user", "lang": "de"}]

def test_get_user_by_id():
  response = client.get("user/0123456789")
  assert response.status_code == 404
