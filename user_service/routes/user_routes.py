from typing import List
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

#import schemas from user-service/models/user_model.py
from user_service.models.user_model import (
    UserModel,
)

#Create FastAPI router 
router = APIRouter()

@router.get("/", response_description="Get all users.", response_model=List[UserModel])
async def list_all_users():
    users = await db["users"].find().to_list(100)
    return users

@router.get(
    "/{userId}", response_description="Read user by id.", response_model=UserModel
)
async def show_user(id: str):
    if (user := await db["user"].find_one({"_id": id})) is not None:
        return user

    raise HTTPException(status_code=404, detail=f"User {id} not found")
