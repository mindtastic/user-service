from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from datetime import datetime
from bson import ObjectId #check bson


class RoleEnum(str, Enum):
    admin = 'admin'
    user = 'user'

class LanguageEnum(str, Enum):
    de = 'de'
    en = 'en'

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# (...) for required fields
class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    role: RoleEnum = RoleEnum.user
    lang: LanguageEnum = LanguageEnum.de
    created: datetime = Field(...)
    changed: datetime = Field(...)


    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "maja",
                "email": "maja@majassen.de",
                "password": "ahcezie2aiKoon0yaequ3eive7uphie9",
                "role": "user",
                "lang": "de",
                "created": "2022-03-07T14:15:44+00:00",
                "changed": "2022-03-07T14:15:44+00:00",
            }
        }
