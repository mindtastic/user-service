from contextlib import contextmanager
from http import client
import logging
import os
from fastapi import FastAPI
import motor.motor_asyncio

MONGO_DETAILS = "mongodb://localhost:27017" # MongoDB details for local testing database

async def connect_to_mongodb(app: FastAPI):
    uri = os.getenv("CONNECTION_STRING")
    #add try except block to handle if the connection string is not set
    try:
        #check if the env variables are empty, if they are, use the local database
        if uri == None:
            client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
            #log info message to console
            logging.info("Connected to localhost:27017")
        else:
            client = motor.motor_asyncio.AsyncIOMotorClient(uri)    
            logging.info("Connected to MongoDB database using env connection string")

        database = client.users # create new database called users
        app.state.user_settings_collection = database.get_collection("user_settings_collection")
        app.state.user_collection = database.get_collection("users_collection")
    except Exception as e:
        # raise configuration error
        print("Error connecting to MongoDB: %s" % e)
        raise e
