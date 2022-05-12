import os
from typing import Optional
from fastapi import FastAPI, HTTPException
import motor.motor_asyncio
from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from datetime import datetime
from bson import ObjectId #check bson

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"], tls=True, tlsAllowInvalidCertificates=True)
db = client.user_service

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



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get(
    "/{id}", response_description="Get a single user", response_model=UserModel
)
async def show_user(id: str):
    if (student := await db["user"].find_one({"_id": id})) is not None:
        return student

    raise HTTPException(status_code=404, detail=f"User {id} not found")
