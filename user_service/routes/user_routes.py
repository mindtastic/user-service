from typing import List, Union
from uuid import UUID
from fastapi import APIRouter, Body, HTTPException, status, Header
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from jsonschema import ValidationError
import logging

#import user settings collection from user-service/database.py
from user_service.database import (
    users_collection,
    user_settings_collection
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
    "",
    response_description="Get all users.",
    response_model=List[UserModelResponse],
    status_code=status.HTTP_200_OK
)
async def show_all_users():
    '''Returns a status code and a list of all users'''
    users = []
    async for user in users_collection.find():
        users.append(user)
    return users

@router.post(
    "", 
    response_description="Add new user",
    response_model=UserModelResponse,
    status_code=status.HTTP_200_OK
)
async def add_new_user(x_user_id: Union[str, None] = Header(default=None), user_data: UserModel = Body(...)):
    '''Creates a new user record'''
    user_data = jsonable_encoder(user_data)
    #adds X-User-Id to user
    user_data["user_id"] = x_user_id

    try:
        await users_collection.insert_one(user_data)
    except ValidationError as error:
        logging.error("Error: %s", error)
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail= error,
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED)

@router.get(
    "",
    response_description="Read user by id.",
    response_model=UserModelResponse,
    status_code=status.HTTP_200_OK
)
async def show_user(x_user_id: Union[str, None] = Header(default=None)):
    '''Returns a single user record'''
    if (user := await users_collection.find_one({"user_id": x_user_id})) is not None:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {x_user_id} not found",
    )

@router.put(
    "",
    response_description="Update user by id.",
    response_model=UserModelResponse,
    status_code=status.HTTP_200_OK
)
async def update_user(x_user_id: Union[str, None] = Header(default=None), user_data: UpdateUserModel = Body(...)):
    '''Updates a single user record'''
    if (await users_collection.find_one({"user_id": x_user_id})) is not None:
        user_data = jsonable_encoder(user_data)
        try:
            await users_collection.update_one(
                {"user_id": x_user_id}, {"$set": user_data}
            )
        except ValidationError as error:
            logging.error("Error: %s", error)
            return HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= error,
            )
        return JSONResponse(status.HTTP_201_CREATED)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {x_user_id} not found",
    )

@router.delete(
    "", 
    response_description="Delete user by user id.",
    status_code=status.HTTP_200_OK
)
async def delete_user(x_user_id: Union[str, None] = Header(default=None)):
    '''Deletes user record'''
    user = await users_collection.find_one({"user_id": x_user_id})
    if user:
        await users_collection.delete_one({"user_id": x_user_id})
        #delete user settings
        await user_settings_collection.delete_one({"user_id": x_user_id})
        return JSONResponse(status.HTTP_200_OK)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {x_user_id} not found",
    )


