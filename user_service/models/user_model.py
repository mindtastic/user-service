from typing import Optional
from enum import Enum
from pydantic import UUID4, BaseModel, Json
from bson import ObjectId #check bson


class RoleEnum(str, Enum):
    admin = 'admin'
    user = 'user'

class LanguageEnum(str, Enum):
    de = 'de'
    en = 'en'

class UserModel(BaseModel):
    user_id: Optional[UUID4]
    username: Optional[str]
    role: RoleEnum = RoleEnum.user
    settings: Optional[Json]


    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "maja",
                "role": "user",
                "settings": {
                  "lang": "de",
                }
            }
        }

class UserModelResponse(BaseModel):
    username: Optional[str]
    role: Optional[RoleEnum]
    settings: Optional[Json]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "maja",
                "role": "user",
                "settings": {
                  "lang": "de",
                }
            }
        }

class UpdateUserModel(BaseModel):
    username: Optional[str]
    role: Optional[RoleEnum]

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "role": "admin",
            }
        }

