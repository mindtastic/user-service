import os
from fastapi import FastAPI
import motor.motor_asyncio
from urllib.parse import quote_plus

MONGO_DETAILS = "mongodb://localhost:27017" # MongoDB details for local testing database

async def connect_to_mongodb(app: FastAPI):
    uri = os.getenv("CONNECTION_STRING", connection_string_from_env())
    #add try except block to handle if the connection string is not set
    try:
        #check if the env variables are empty, if they are, use the local database
        if uri is None:
            client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
            print("Connected to localhost:27017")
        else:
            client = motor.motor_asyncio.AsyncIOMotorClient(uri)
            print("Connected to MongoDB database using env connection string")
        await client.admin.command("ismaster")

        database = client.users # create new database called users
        app.state.user_settings_collection = database.get_collection("user_settings_collection")
        app.state.user_collection = database.get_collection("users_collection")
    except Exception as e:
        # raise configuration error
        print("Error connecting to MongoDB: %s" % e)
        raise e

def connection_string_from_env() -> str:
    return "mongodb://%s:%s@%s/%s?authSource=%s" % (
            quote_plus(os.getenv('MONGODB_USER', 'admin')),
            quote_plus(os.getenv('MONGODB_PASSWORD', 'admin')),
            quote_plus(os.getenv('MONGODB_HOST')),
            quote_plus(os.getenv('MONGODB_DB')),
            quote_plus(os.getenv('MONGODB_AUTHSOURCE', 'admin'))
        )
