from http import client
from fastapi.testclient import TestClient
from user_service.app import app
import user_service.database as database
import mongomock
import logging


client = TestClient(app) #create test client
with database.ClientManager() as db_client:
    db_client = mongomock.MongoClient()
    logging.info("Connected to mongomock database")  
    print('here')

#test root endpoint
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

#run tests with pytest, after "pip install pytest" and "pip install requests"
