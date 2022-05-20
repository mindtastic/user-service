from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

#import user settings collection from user-service/database.py
from user_service.database import (
    user_settings_collection,
    users_collection
)

#import schemas from user-service/models/user_settings_model.py
from user_service.models.user_settings_model import (
    UserSettingsSchema,
    UserSettingsResponse
)

#Create FastAPI router 
router = APIRouter()

# Create GET endpoint for user settings by user id
# TODO add Unauthorized error
@router.get("/{user_id}/settings", response_description="Retrieve user settings by user id", response_model=UserSettingsResponse)
async def get_user_settings_by_id(user_id: int):
    """
    Get user settings by user id
    """
    #check if user exists
    user = await users_collection.find_one({"userId": user_id})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    #get user settings
    user_settings = await user_settings_collection.find_one({"userId": user_id})
    if user_settings is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User settings not found")
    
    #return user settings
    return user_settings


# Create POST endpoint for user settings by user id
# TODO add Unauthorized error
@router.post("/{user_id}/settings", response_description="Add user settings by user id", response_model=UserSettingsResponse)
async def create_user_settings(user_id: int, user_settings: UserSettingsSchema):
    """
    Add user settings by user id
    """
    #check if user exists
    user = await users_collection.find_one({"userId": user_id})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    #create user settings
    user_settings.userId = user_id
    user_settings_id = await user_settings_collection.insert_one(user_settings)
    user_settings.id = str(user_settings_id.inserted_id)
    
    #return user settings
    return JSONResponse(status_code=status.HTTP_200_OK)


# Create DELETE endpoint for deleting user settings by user id
# TODO add Unauthorized error
@router.delete("/{user_id}/settings", response_description="Delete user settings by user id")
async def delete_user_settings(user_id: int):
    """
    Delete user settings by user id
    """
    #check if user exists
    user = await users_collection.find_one({"userId": user_id})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    #delete user settings
    await user_settings_collection.delete_one({"userId": user_id})
    return JSONResponse(status_code=status.HTTP_200_OK)

