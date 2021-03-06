from http import client
from fastapi.testclient import TestClient
from user_service.app import app

client = TestClient(app) #create test client

#test root endpoint
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

#run tests with pytest, after "pip install pytest" and "pip install requests"
