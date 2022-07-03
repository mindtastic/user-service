from typing import Optional, Dict
from enum import Enum
from pydantic import UUID4, BaseModel
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
    settings: Dict[str, str]


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
    settings: Dict[str, str]

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

