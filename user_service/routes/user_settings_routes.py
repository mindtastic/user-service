import logging
from typing import Union
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Body, Header
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from jsonschema import ValidationError
from user_service.routes.dependencies import get_mongo_collection, ServiceDBCollection

#import schemas from user-service/models/user_settings_model.py
from user_service.models.user_settings_model import (
    UserSettingsSchema,
    UserSettingsResponse,
)

#Create FastAPI router
router = APIRouter()

@router.get(
    "/settings",
    response_description="Retrieve user settings by user id",
    response_model=UserSettingsResponse,
    status_code=status.HTTP_200_OK
)
async def get_user_settings_by_id(
    X_User_Id: Union[UUID, None] = Header(default=None),
    users_collection = Depends(get_mongo_collection(ServiceDBCollection.USERS)),
    user_settings_collection = Depends(get_mongo_collection(ServiceDBCollection.SETTINGS))
):
    """
    Get user settings by user id
    """
    #check if user exists
    user = await users_collection.find_one({"user_id": X_User_Id})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {X_User_Id} not found"
        )
    #get user settings
    try:
        user_settings = await user_settings_collection.find_one({"user_id": X_User_Id})
    except ValidationError as error:
        logging.error("Error: %s", error)
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail= error,
        )
    if user_settings is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User settings not found"
        )
    return user_settings


@router.post(
    "/settings",
    response_description="Add user settings by user id",
    response_model=UserSettingsResponse
)
async def create_user_settings(
    X_User_Id: Union[UUID, None] = Header(default=None), 
    user_settings: UserSettingsSchema = Body(...),
    users_collection = Depends(get_mongo_collection(ServiceDBCollection.USERS)),
    user_settings_collection = Depends(get_mongo_collection(ServiceDBCollection.SETTINGS))
):
    """
    Add user settings by user id
    """
    #check if user exists
    user = await users_collection.find_one({"user_id": X_User_Id})

    try:
        if user is not None:
            #add X_User_Id header parameter to user settings model
            user_settings_dict = user_settings.dict()
            user_settings_dict.update({"user_id": X_User_Id})
            await user_settings_collection.insert_one(user_settings_dict)
            return JSONResponse(status_code=status.HTTP_200_OK)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {X_User_Id} not found"
            )
    except ValidationError as error:
        logging.error("Error: %s", error)
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail= error,
    )

# Create DELETE endpoint for deleting user settings by user id
@router.delete(
    "/settings", 
    response_description="Delete user settings by user id")
async def delete_user_settings(
    X_User_Id: Union[UUID, None] = Header(default=None),
    users_collection = Depends(get_mongo_collection(ServiceDBCollection.USERS)),
    user_settings_collection = Depends(get_mongo_collection(ServiceDBCollection.SETTINGS))):
    """
    Delete user settings by user id
    """
    #check if user exists
    user = await users_collection.find_one({"user_id": X_User_Id})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    #check if user settings exists
    user_settings = await user_settings_collection.find_one({"user_id": X_User_Id})
    if user_settings is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User settings not found")

    #otherwise delete user settings
    await user_settings_collection.delete_one({"user_id": X_User_Id})
    return JSONResponse(status_code=status.HTTP_200_OK)
