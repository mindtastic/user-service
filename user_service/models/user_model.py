from typing import Optional, Dict
from enum import Enum
from pydantic import UUID4, BaseModel, EmailStr, validator
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
    email: Optional[EmailStr]
    role: RoleEnum = RoleEnum.user
    settings: Optional[Dict[str, str]]

    @validator('settings', pre=True)
    def add_default_lang(cls, v):
        '''Adds default language if none given'''
        if "lang" not in v.keys():
            return {"lang": LanguageEnum.de}
        return v

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "username": "maja",
                "role": "user",
                "email": "maja@example.com",
                "settings": {
                  "lang": "de",
                }
            }
        }

class UserModelResponse(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    role: Optional[RoleEnum]
    settings: Optional[Dict[str, str]]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "maja",
                "role": "user",
                "email": "maja@example.com",
                "settings": {
                  "lang": "de",
                }
            }
        }

class UpdateUserModel(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    role: Optional[RoleEnum]
    settings: Optional[Dict[str, str]]

    class Config:
        schema_extra = {
            "example": {
                "username": "maja",
                "role": "user",
                "email": "maja@example.com",
                "settings": {
                  "lang": "de",
                }
            }
        }

    @validator('settings')
    def check_language(cls, v):
        '''Checks if language is of available language'''
        if not v.get("lang"):
            return v
        if v.get("lang") in set(item.value for item in LanguageEnum):
            return v
        raise ValueError('Language is not available, must be "de" or "eng"')
