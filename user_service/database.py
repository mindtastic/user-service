import os
import motor.motor_asyncio
from urllib.parse import quote_plus

MONGO_DETAILS = "mongodb://localhost:27017" # MongoDB details for local testing database
user = os.getenv('MONGO_INITDB_ROOT_USERNAME', "admin")
password = os.getenv('MONGO_INITDB_PASSWORD',  "test123")
databaseHost = os.getenv('MONGODB_HOST', "mongodb_user_service")
uri = "mongodb://%s:%s@%s" % (quote_plus(user), quote_plus(password), databaseHost)

#add try except block to handle if the database is not available
try:
    client = motor.motor_asyncio.AsyncIOMotorClient(uri)
    db = client.user_service
    print("Connected to MongoDB")
except Exception as e:
    print("Could not connect to MongoDB: %s" % e)

database = client.users # create new database called users

# create and get collections (akin to tables)
user_settings_collection = database.get_collection("user_settings_collection")
users_collection = database.get_collection("users_collection")
