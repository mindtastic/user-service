from typing import Optional
from enum import Enum
import uuid
from pydantic import BaseModel, Field
from bson import ObjectId #check bson


class RoleEnum(str, Enum):
    admin = 'admin'
    user = 'user'

# (...) for required fields
class UserModel(BaseModel):
    account_key: uuid = Field(...)
    username: str = Field(...)
    role: RoleEnum = RoleEnum.user


    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "account_key": "123e4567-e89b-12d3-a456-426655440000",
                "username": "maja",
                "role": "user",
            }
        }

class UserModelResponse(BaseModel):
    username: str = Field(...)
    role: RoleEnum = RoleEnum.user

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "maja",
                "role": "user",
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
