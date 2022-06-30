from contextlib import contextmanager
from http import client
import logging
import os
from fastapi import Depends
import motor.motor_asyncio
from urllib.parse import quote_plus

MONGO_DETAILS = "mongodb://localhost:27017" # MongoDB details for local testing database
uri = os.getenv("CONNECTION_STRING")


#add try except block to handle if the connection string is not set
try:
    #check if the env variables are empty, if they are, use the local database
    if uri == None:
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
        print("Connected to localhost:27017")
    else:
        client = motor.motor_asyncio.AsyncIOMotorClient(uri)    
        print("Connected to MongoDB database using env connection string")
except Exception as e:
    # raise configuration error
    print("Error connecting to MongoDB: %s" % e)
    raise e


@contextmanager
def ClientManager():
    try:
        yield client
    except Exception as e:
        logging.error(e)
        raise e

with ClientManager() as db_client:
    database = db_client.users # get database called users
    # create and get collections (akin to tables)
    user_settings_collection = database.get_collection("user_settings_collection")
    users_collection = database.get_collection("users_collection")
