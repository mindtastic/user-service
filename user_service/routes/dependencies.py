import enum
from typing import Callable
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.requests import Request

class ServiceDBCollection(enum.Enum):
    SETTINGS = 1
    USERS = 2

def _get_settings_collection(request: Request):
    return request.app.state.user_settings_collection

def _get_users_collection(request: Request):
    return request.app.state.user_collection

def get_mongo_collection(collection: ServiceDBCollection) -> Callable:
    if collection == ServiceDBCollection.SETTINGS:
        def _get_settings(db = Depends(_get_settings_collection)):
            return db

        return _get_settings
    elif collection == ServiceDBCollection.USERS:
        def _get_users(db = Depends(_get_users_collection)):
            return db
        
        return _get_users
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
