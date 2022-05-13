import motor.motor_asyncio

MONGO_DETAILS = "mongodb://localhost:27017" # MongoDB details for local testing database

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.user_settings # create new database called user_settings

user_settings_collection = database.get_collection("user_settings_collection") # create and get a collection called user_settings_collection

