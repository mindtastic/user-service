import os
import motor.motor_asyncio
from urllib.parse import quote_plus

MONGO_DETAILS = "mongodb://localhost:27017" # MongoDB details for local testing database
user = os.getenv('MONGO_INITDB_ROOT_USERNAME', "")
password = os.getenv('MONGO_INITDB_PASSWORD',  "")
databaseHost = os.getenv('MONGODB_HOST', "")
uri = "mongodb://%s:%s@%s" % (quote_plus(user), quote_plus(password), databaseHost)

#add try except block to handle if the database is not available
try:
    #check if the env variables are empty, if they are, use the local database
    if user == "" or password == "":
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
    else:
        client = motor.motor_asyncio.AsyncIOMotorClient(uri)    
    print("Connected to MongoDB")
except Exception as e:
    # raise configuration error
    print("Error connecting to MongoDB: %s" % e)
    raise e



database = client.users # create new database called users

# create and get collections (akin to tables)
user_settings_collection = database.get_collection("user_settings_collection")
users_collection = database.get_collection("users_collection")
