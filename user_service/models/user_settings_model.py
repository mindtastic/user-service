from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum
from bson import ObjectId

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
        field_schema.update(type="integer")

class UserSettingsSchema(BaseModel):
    id : PyObjectId = Field(alias="_id", default_factory=PyObjectId)
    userId : int = Field(...)
    language: LanguageEnum = LanguageEnum.de #Default value is "de"
    #TODO more settings to be added here
    
    class Config:
        allow_population_by_field_name = True
        use_enum_values = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "userId": 1,
                "language": "de"
            }
        }

#TODO check if this is needed
class UpdateUserSettingsModel(BaseModel):
    userId : int = Field(...)
    language: Optional[LanguageEnum]
    #more settings to be added here
    
    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "userId": 1,
                "language": "de"
            }
        }

    