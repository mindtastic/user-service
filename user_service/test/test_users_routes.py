from http import client
import json
from fastapi.testclient import TestClient
from user_service.app import app

client = TestClient(app) #create test client

USERDATA = {
  "id": "1",
  "username": "test",
  "email": "test@test.com",
  "role": "user",
  "lang": "de"
}

# test create user endpoint
def test_create_user():
    response = client.post("user/", json.dumps(USERDATA))
    assert response.status_code == 200
    assert response.json()["email"] == "test@test.com"
    assert response.json()["lang"] == "de"

# test get /user endpoint
def test_get_all_users():
    response = client.get("user/")
    assert response.status_code == 200
    assert response.json() == [USERDATA]

# test get /user/{id} enpoint
def test_get_user_by_id():
    response = client.get("user/0123456789")
    assert response.status_code == 404

# test put /user/{id} endpoint
def update_user_by_id():
    response = client.put("user/1", json.dumps({"username": "updated_test"}))
    assert response.status_code == 200
    assert response.json()["username"] == "updated_test"
