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

""" #Create ResponseModel with optional data field
def ResponseModel(data, message):
    return {
        "data": Optional[data],
        "code": 200,
        "message": Optional[message]
    } """

#Create Error response model for the error responses from endpoints
def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }
    

#Create Response model class for the response from the endpoints
class ResponseModel(BaseModel):
    data: Optional[dict]
    code: int
    message: Optional[str]
    