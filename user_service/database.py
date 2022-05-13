import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017" # MongoDB details for local testing database

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.user_settings # create new database called user_settings

user_settings_collection = database.get_collection("user_settings_collection") # create new collection called user_settings_collection

# User settings helper function
def user_settings_helper(user_settings) -> dict:
    return {
        "userId": int(user_settings["userId"]),
        "language": user_settings["language"]
        # Add more settings here
    }

# Add new user settings into to the database by user ID
async def add_new_user_settings_by_id(id: int, data: dict):
    user_settings = await user_settings_collection.find_one({"userId": ObjectId(id)})
    if user_settings:
        updated_user_settings = await user_settings_collection.update_one(
            {"userId": ObjectId(id)}, {"$set": data}
        )
        if updated_user_settings:
            return True
        return False

# Retrieve the user settings by ID from the database
async def retrieve_user_settings_by_id(id: int) -> dict:
    user_settings = await user_settings_collection.find_one({"userId": ObjectId(id)})
    if user_settings:
        return user_settings_helper(user_settings)


# Update user settings by user ID in database - this is not in the initial API documentation but added here
async def update_user_settings_by_id(id: int, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user_settings = await user_settings_collection.find_one({"userId": ObjectId(id)})
    if user_settings:
        updated_user_settings = await user_settings_collection.update_one(
            {"userId": ObjectId(id)}, {"$set": data}
        )
        if updated_user_settings:
            return True
        return False

# Delete user's settings from database by user ID
async def delete_user_settings_by_id(id: int):
    user_settings = await user_settings_collection.find_one({"userId": ObjectId(id)})
    if user_settings:
        await user_settings_collection.delete_one({"userId": ObjectId(id)})
        return True
