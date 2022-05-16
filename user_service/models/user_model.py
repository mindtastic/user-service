from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from bson import ObjectId #check bson


class RoleEnum(str, Enum):
    admin = 'admin'
    user = 'user'

class LanguageEnum(str, Enum):
    de = 'de'
    en = 'en'

# (...) for required fields
class UserModel(BaseModel):
    id: str = Field(...)
    username: str = Field(...)
    email: EmailStr = Field(...)
    role: RoleEnum = RoleEnum.user
    lang: LanguageEnum = LanguageEnum.de


    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "maja",
                "email": "maja@majassen.de",
                "role": "user",
                "lang": "de",
            }
        }

class UserModelResponse(BaseModel):
    id: str = Field(...)
    username: str = Field(...)
    email: EmailStr = Field(...)
    role: RoleEnum = RoleEnum.user
    lang: LanguageEnum = LanguageEnum.de


    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "maja",
                "email": "maja@majassen.de",
                "role": "user",
                "lang": "de",
            }
        }

class UpdateUserModel(BaseModel):
  username: Optional[str]
  email: Optional[EmailStr]
  role: Optional[RoleEnum]
  lang: Optional[LanguageEnum]

  class Config:
    schema_extra = {
      "example": {
        "username": "string",
        "email": "user@example.com",
        "role": "admin",
        "lang": "de",
      }
    }
