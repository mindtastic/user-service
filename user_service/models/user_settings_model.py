from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class LanguageEnum(str, Enum):
    de = 'de'
    en = 'en'


class UserSettingsSchema(BaseModel):
    userId : int = Field(..., description="The user id")
    language: LanguageEnum = LanguageEnum.de #Default value is "de"
    #TODO more settings to be added here
    
    class Config:
        use_enum_values = True
        schema_extra = {
            "example": {
                "userId": 1,
                "language": "de"
            }
        }

#TODO check if this is needed
class UpdateUserSettingsModel(BaseModel):
    userId : Optional[int] = Field(None, description="The user id")
    language: Optional[LanguageEnum]
    #more settings to be added here
    
    class Config:
        use_enum_values = True
        schema_extra = {
            "example": {
                "language": "de"
            }
        }

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message
    }

def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }
    