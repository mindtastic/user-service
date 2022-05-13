from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class LanguageEnum(str, Enum):
    de = 'de'
    en = 'en'


class UserSettingsSchema(BaseModel):
    userId : str = Field(alias="_id")
    language: LanguageEnum = LanguageEnum.de
    #more settings to be added here
    
    class Config:
        use_enum_values = True
        schema_extra = {
            "example": {
                "userId": "5e8f8f8f8f8f8f8f8f8f8f8",
                "language": "de"
            }
        }
