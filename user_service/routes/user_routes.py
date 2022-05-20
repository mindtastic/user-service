from email.policy import default
from typing import List
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from jsonschema import ValidationError

#import user settings collection from user-service/database.py
from user_service.database import (
    users_collection,
)

#import schemas from user-service/models/user_model.py
from user_service.models.user_model import (
    UserModel,
    UpdateUserModel,
    UserModelResponse,
)

#Create FastAPI router
router = APIRouter()

@router.get(
    "/",
    response_description="Get all users.",
    response_model=List[UserModelResponse],
)
async def show_all_users():
    users = []
    async for user in users_collection.find():
        users.append(user)
    return users

@router.post(
    "/", response_description="Add new user", response_model=UserModelResponse
)
async def add_new_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    print(user["role"])
    try:
        await users_collection.insert_one(user)
    except ValidationError as error:
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail= error,
    )

    return JSONResponse(status_code=status.HTTP_200_OK)

@router.get(
    "/{userId}",
    response_description="Read user by id.",
    response_model=UserModelResponse,
)
async def show_user(userId: str):
    if (user := await users_collection.find_one({"userId": userId})) is not None:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {id} not found",
    )

@router.put(
    "/{userId}",
    response_description="Update user by id.",
    response_model=UserModelResponse,
)
async def update_user(userId: str, user_data: UpdateUserModel = Body(...)):
    if (await users_collection.find_one({"userId": userId})) is not None:
        user_data = jsonable_encoder(user_data)
        try:
            await users_collection.update_one(
                {"userId": userId}, {"$set": user_data}
            )
        except ValidationError as error:
            return HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= error,
            )
        return JSONResponse(status.HTTP_200_OK)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User {userId} not found",
    )

@router.delete("/{userId}", response_description="Delete user by user id.")
async def delete_user(userId: str):
    user = await users_collection.find_one({"userId": userId})
    if user:
        await users_collection.delete_one({"userId": userId})
        return JSONResponse(status.HTTP_200_OK)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User {userId} not found",
    )
