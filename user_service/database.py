import motor.motor_asyncio

MONGO_DETAILS = "mongodb://localhost:27017" # MongoDB details for local testing database

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.users # create new database called users

# create and get collections (akin to tables)
user_settings_collection = database.get_collection("user_settings_collection")
users_collection = database.get_collection("users_collection")
