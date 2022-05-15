from typing import List
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

#import user settings collection from user-service/database.py
from user_service.database import (
    users_collection
)

#import schemas from user-service/models/user_model.py
from user_service.models.user_model import (
    UserModel,
)

#Create FastAPI router 
router = APIRouter()

@router.get(
    "/{userId}", response_description="Read user by id.", response_model=UserModel
)
async def show_user(userId: int):
    if (user := await users_collection.find_one({"userId": userId})) is not None:
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found")
