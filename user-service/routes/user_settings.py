from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

#import database functions from user-service/database.py
from database import (
    add_new_user_settings_by_id, 
    retrieve_user_settings_by_id, 
    update_user_settings_by_id, 
    delete_user_settings_by_id,
)

#import schemas from user-service/models/user_settings_model.py
from models.user_settings_model import (
    UserSettingsSchema,
    UpdateUserSettingsModel,
    ResponseModel,
    ErrorResponseModel,
)

#Create FastAPI router 
router = APIRouter()

#Create POST endpoint for adding new user settings
#TODO add Unauthorized error
@router.post("/", response_model=ResponseModel, status_code=200, response_description="User settings created")
async def add_new_user_settings(user_settings: UserSettingsSchema):
    user_settings_data = jsonable_encoder(user_settings)
    if await add_new_user_settings_by_id(user_settings_data["userId"], user_settings_data):
        return ResponseModel(
            message="User settings successfully added",
            status_code=200,
        )
    return ErrorResponseModel(
        message="User settings could not be added",
        status_code=500,
    )

# Create GET endpoint for retrieving user settings by user id
#TODO add Unauthorized error    
@router.get("/{user_id}", response_model=ResponseModel, status_code=200, response_description="User settings retrieved")
async def retrieve_user_settings(user_id: str):
    if user_settings := await retrieve_user_settings_by_id(user_id):
        return ResponseModel(
            message="User settings retrieved",
            status_code=200,
            data=user_settings,
        )
    return ErrorResponseModel(
        message="User settings could not be retrieved",
        status_code=500,
    )