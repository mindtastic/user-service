from loguru import logger
import os
from fastapi import FastAPI
import motor.motor_asyncio
from urllib.parse import quote_plus

async def connect_to_mongodb(app: FastAPI):
    connection_string = os.getenv("CONNECTION_STRING", None)
    
    #add try except block to handle if the connection string is not set
    try:
        #check if the env variables are empty, if they are, use the local database
        if connection_string is None:
            buildin_connection_string = connection_string_from_env()
            client = motor.motor_asyncio.AsyncIOMotorClient(buildin_connection_string)
            logger.info(f"Connected to MongoDB from build-in connection string {buildin_connection_string}")
        else:
            client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
            logger.info("Connected to MongoDB database using env connection string")
        
        await client.admin.command("ismaster")

        database = client.users # create new database called users
        app.state.user_settings_collection = database.get_collection("user_settings_collection")
        app.state.user_collection = database.get_collection("users_collection")
    except Exception as e:
        # raise configuration error
        logger.error("Error connecting to MongoDB: %s" % e)
        raise e

def connection_string_from_env() -> str:
    return "mongodb://%s:%s@%s/%s?authSource=%s" % (
            quote_plus(os.getenv('MONGODB_USER', 'admin')),
            quote_plus(os.getenv('MONGODB_PASSWORD', 'admin')),
            quote_plus(os.getenv('MONGODB_HOST', 'mongo_user')),
            quote_plus(os.getenv('MONGODB_DB', 'users')),
            quote_plus(os.getenv('MONGODB_AUTHSOURCE', 'admin'))
        )
