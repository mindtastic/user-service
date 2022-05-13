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

