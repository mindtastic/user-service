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
        allow_population_by_field_name = True
        use_enum_values = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "userId": 1,
                "language": "de"
            }
        }

#TODO check if this is needed
class UpdateUserSettingsModel(BaseModel):
    language: Optional[LanguageEnum]
    #more settings to be added here
    
    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "language": "de"
            }
        }

    