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
    UpdateUserModel
)

#Create FastAPI router 
router = APIRouter()

@router.get(
  "/", response_description="Get all users.", response_model=List[UserModel]
)
async def show_all_users():
  users = []
  async for user in users_collection.find():
      users.append(user)
  return users

@router.post("/{userId}", response_description="Add new user settings", response_model=UserModel)
async def add_new_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    await users_collection.insert_one(user)
    return JSONResponse(status_code=status.HTTP_200_OK, detail="User created")

@router.get(
    "/{userId}", response_description="Read user by id.", response_model=UserModel
)
async def show_user(userId: int):
  if (user := await users_collection.find_one({"userId": userId})) is not None:
      return user

  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found")

@router.put(
  "/{userId}", response_description="Update user by id.", response_model=UpdateUserModel
)
async def update_user(userId: int, user_data: UpdateUserModel = Body(...)):
  user_data = jsonable_encoder(user_data)
  updated_user_data = await users_collection.update_one(
      {"userId": userId}, {"$set": user_data}
  )
  if updated_user_data:
      return JSONResponse(status.HTTP_200_OK)
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User {userId} not found")

@router.delete("/{userId}", response_description="Delete user by user id.")
async def delete_user(userId: int):
    user = await users_collection.find_one({"userId": userId})
    if user:
        await users_collection.delete_one({"userId": userId})
        return JSONResponse(status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User {userId} not found")
