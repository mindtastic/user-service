from typing import List, Union
from uuid import UUID
from user_service.routes.dependencies import get_mongo_collection, ServiceDBCollection
from fastapi import APIRouter, Body, HTTPException, status, Header, Depends
from fastapi.responses import JSONResponse
from jsonschema import ValidationError
import logging
from user_service.tilt.user_service_tilt import tilt_dict
from user_service.models.user_model import (
    UserModel,
    UpdateUserModel,
    UserModelResponse,
)

#Create FastAPI router
router = APIRouter()

#Default user data
default_user_data = {
    "username": "",
    "role": "user",
    "settings": {
      "lang": "de"
    }
}

#Default user settings
default_settings = {
    "settings": {
      "lang": "de"
    }
}

@router.get(
    "/admin/user",
    response_description="Get all users.",
    response_model=List[UserModelResponse],
    status_code=status.HTTP_200_OK
)
async def show_all_users(
    users_collection = Depends(get_mongo_collection(ServiceDBCollection.USERS)),
    users_settings_collection = Depends(get_mongo_collection(ServiceDBCollection.SETTINGS))):
    '''Returns a status code and a list of all users'''
    users = []
    async for user in users_collection.find():
        user_settings = await users_settings_collection.find_one(
            {"user_id": user["user_id"]},
            {"lang": 1, "_id": False},
        )
        user.update({"settings": user_settings})
        users.append(user)
    return users

@router.post(
    "/admin/user",
    response_description="Add new user",
    status_code=status.HTTP_200_OK,
)
async def add_new_user(
    X_User_Id: Union[UUID, None] = Header(default=None),
    users_collection = Depends(get_mongo_collection(ServiceDBCollection.USERS)),
    users_settings_collection = Depends(get_mongo_collection(ServiceDBCollection.SETTINGS)),
    user_data: UserModel = Body(...)):
    '''Creates a new user record'''
    user_data_dict = user_data.dict()
    user_data_dict.update({"user_id": X_User_Id})
    user_settings_data_dict = user_data_dict.pop('settings') or default_settings
    user_settings_data_dict.update({"user_id": X_User_Id})
    try:
        await users_collection.insert_one(user_data_dict)
        await users_settings_collection.insert_one(user_settings_data_dict)
    except ValidationError as error:
        logging.error("Error: %s", error)
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail= error,
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED)

@router.get(
    "/user",
    response_description="Get data of current user",
    response_model=UserModelResponse,
    status_code=status.HTTP_200_OK
)
async def show_user(
    X_User_Id: Union[UUID, None] = Header(default=None),
    users_collection = Depends(get_mongo_collection(ServiceDBCollection.USERS)),
    users_settings_collection = Depends(get_mongo_collection(ServiceDBCollection.SETTINGS))
):
    #return user by id, if user is not found, create new user with empty Body
    if (user := await users_collection.find_one({"user_id": X_User_Id})) is not None:
        # returns only the language from settings
        # if we want to add more settings to be returned in the future
        # add {"column": 1} to line 87
        user_settings = await users_settings_collection.find_one(
            {"user_id": X_User_Id},
            {"lang": 1, "_id": False},
        )
        user.update({"settings": user_settings})
        return user

    await add_new_user(
        X_User_Id=X_User_Id,
        user_data=UserModel(**default_user_data),
        users_collection=users_collection,
        users_settings_collection=users_settings_collection,
    )

    new_user = await users_collection.find_one({"user_id": X_User_Id})
    new_user_settings = await users_settings_collection.find_one(
            {"user_id": X_User_Id},
            {"lang": 1, "_id": False},
        )
    new_user.update({"settings": new_user_settings})
    return new_user

@router.put(
    "/user",
    response_description="Update data of authenticated user",
    response_model=UserModelResponse,
    status_code=status.HTTP_200_OK
)
async def update_user(
    X_User_Id: Union[UUID, None] = Header(default=None), 
    users_collection = Depends(get_mongo_collection(ServiceDBCollection.USERS)),
    user_data: UpdateUserModel = Body(...)):
    '''Updates a single user record'''
    if (await users_collection.find_one({"user_id": X_User_Id})) is not None:
        user_update = user_data.dict(exclude_unset=True, exclude={'settings'})
        user_settings_update = user_data.dict(exclude_unset=True, include={'settings'})
        try:
            if bool(user_update):
                await users_collection.update_one(
                    {"user_id": X_User_Id}, {"$set": user_update}
                )
            if bool(user_settings_update.get("settings")):
                await users_collection.update_one(
                    {"user_id": X_User_Id}, {"$set": user_settings_update}
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
    "/user",
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

#Get endpoint for exposing TILT spec, return tilt_dict from user_service/tilt/user_service_tilt.py file
@router.get(
    "/tilt/user",
    response_description="Get TILT spec.",
    response_model=dict,
    status_code=status.HTTP_200_OK
)
async def get_tilt_spec():
    return tilt_dict
