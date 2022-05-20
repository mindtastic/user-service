from fastapi import APIRouter, HTTPException, status, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

#import user settings collection from user-service/database.py
from user_service.database import (
    user_settings_collection,
    users_collection,
)

#import schemas from user-service/models/user_settings_model.py
from user_service.models.user_settings_model import (
    UserSettingsSchema,
    UserSettingsResponse,
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
    user = await users_collection.find_one({"userId": str(user_id)}) #TODO change to user_id - after alignment with Isabel regarding the type
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
async def create_user_settings(user_id: int, user_settings: UserSettingsSchema = Body(...)):
    """
    Add user settings by user id
    """
    #check if user exists
    user = await users_collection.find_one({"userId": str(user_id)})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    #check that user settings do not exist
    user_settings_exists = await user_settings_collection.find_one({"userId": user_id})
    if user_settings_exists is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User settings already exists")
    
    user_settings = jsonable_encoder(user_settings)
    await user_settings_collection.insert_one(user_settings)
    return JSONResponse(status_code=status.HTTP_200_OK)


# Create DELETE endpoint for deleting user settings by user id
# TODO add Unauthorized error
@router.delete("/{user_id}/settings", response_description="Delete user settings by user id")
async def delete_user_settings(user_id: int):
    """
    Delete user settings by user id
    """
    #check if user exists
    user = await users_collection.find_one({"userId": str(user_id)})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    #check if user settings exists
    user_settings = await user_settings_collection.find_one({"userId": user_id})
    if user_settings is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User settings not found")

    #otherwise delete user settings
    await user_settings_collection.delete_one({"userId": user_id})
    return JSONResponse(status_code=status.HTTP_200_OK)

