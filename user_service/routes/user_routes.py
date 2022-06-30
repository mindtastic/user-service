from typing import List, Union
from uuid import UUID
from user_service.routes.dependencies import get_mongo_collection, ServiceDBCollection
from fastapi import APIRouter, Body, HTTPException, status, Header, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from jsonschema import ValidationError
import logging

#import schemas from user-service/models/user_model.py
from user_service.models.user_model import (
    UserModel,
    UpdateUserModel,
    UserModelResponse,
)

#Create FastAPI router
router = APIRouter()

@router.get(
    "s/admin",
    response_description="Get all users.",
    response_model=List[UserModelResponse],
    status_code=status.HTTP_200_OK
)
async def show_all_users(users_collection = Depends(get_mongo_collection(ServiceDBCollection.USERS))):
    '''Returns a status code and a list of all users'''
    users = []
    async for user in users_collection.find():
        users.append(user)
    return users

@router.post(
    "s/admin", 
    response_description="Add new user",
    response_model=UserModelResponse,
    status_code=status.HTTP_200_OK
)
async def add_new_user(
    X_User_Id: Union[UUID, None] = Header(default=None), 
    users_collection = Depends(get_mongo_collection(ServiceDBCollection.USERS)),
    user_data: UserModel = Body(...)):
    '''Creates a new user record'''
    user_data_dict = user_data.dict()
    user_data_dict.update({"user_id": X_User_Id})
    #user_data = jsonable_encoder(user_data)

    try:
        await users_collection.insert_one(user_data_dict)
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
async def show_user(
    X_User_Id: Union[UUID, None] = Header(default=None),
    users_collection = Depends(get_mongo_collection(ServiceDBCollection.USERS))
):
    '''Returns a single user record'''
    if (user := await users_collection.find_one({"user_id": X_User_Id})) is not None:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {X_User_Id} not found",
    )

@router.put(
    "",
    response_description="Update user by id.",
    response_model=UserModelResponse,
    status_code=status.HTTP_200_OK
)
async def update_user(
    X_User_Id: Union[UUID, None] = Header(default=None), 
    users_collection = Depends(get_mongo_collection(ServiceDBCollection.USERS)),
    user_data: UpdateUserModel = Body(...)):
    '''Updates a single user record'''
    if (await users_collection.find_one({"user_id": X_User_Id})) is not None:
        user_data = jsonable_encoder(user_data)
        try:
            await users_collection.update_one(
                {"user_id": X_User_Id}, {"$set": user_data}
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
        detail=f"User {X_User_Id} not found",
    )

@router.delete(
    "", 
    response_description="Delete user by user id.",
    status_code=status.HTTP_200_OK
)
async def delete_user(
    X_User_Id: Union[UUID, None] = Header(default=None),
    users_collection = Depends(get_mongo_collection(ServiceDBCollection.USERS)),
    user_settings_collection = Depends(get_mongo_collection(ServiceDBCollection.SETTINGS))
):
    '''Deletes user record'''
    user = await users_collection.find_one({"user_id": X_User_Id})
    if user:
        await users_collection.delete_one({"user_id": X_User_Id})
        #delete user settings
        await user_settings_collection.delete_one({"user_id": X_User_Id})
        return JSONResponse(status.HTTP_200_OK)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {X_User_Id} not found",
    )


