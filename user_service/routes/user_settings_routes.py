from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

#import user settings collection from user-service/database.py
from user_service.database import (
    user_settings_collection
)

#import schemas from user-service/models/user_settings_model.py
from user_service.models.user_settings_model import (
    UserSettingsSchema,
    UpdateUserSettingsModel,
    UserSettingsResponse
)

#Create FastAPI router 
router = APIRouter()

#Create POST endpoint for adding new user settings
#TODO add Unauthorized error
@router.post("/{userId}/settings", response_description="Add new user settings", response_model=UserSettingsSchema)
async def add_new_user_settings(user_settings: UserSettingsSchema = Body(...)):
    user_settings = jsonable_encoder(user_settings)
    await user_settings_collection.insert_one(user_settings)
    return JSONResponse(status_code=status.HTTP_200_OK, detail="User settings created")

# Create GET endpoint for retrieving user settings by user ID
# TODO add Unauthorized error
@router.get("/{userId}/settings", response_description="Retrieve user settings by user id", response_model=UserSettingsResponse)
async def retrieve_user_settings_by_id(userId: int):
    user_settings = await user_settings_collection.find_one({"userId": userId})
    if user_settings:
        return user_settings
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User settings not found")   

# Create PUT endpoint for updating user settings by user ID
#TODO add Unauthorized error
@router.put("/{userId}/settings", response_description="Update user settings by user id", response_model=UserSettingsSchema)
async def update_user_settings_by_id(userId: int, user_settings: UpdateUserSettingsModel):
    user_settings = jsonable_encoder(user_settings)
    updated_user_settings = await user_settings_collection.update_one(
        {"userId": userId}, {"$set": user_settings}
    )
    if updated_user_settings:
        return JSONResponse(status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User settings not found")

# Create DELETE endpoint for deleting user settings by user ID
#TODO add Unauthorized error
@router.delete("/{userId}/settings", response_description="Delete user settings by user id")
async def delete_user_settings_by_id(userId: int):
    user_settings = await user_settings_collection.find_one({"userId": userId})
    if user_settings:
        await user_settings_collection.delete_one({"userId": userId})
        return JSONResponse(status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User settings not found")
