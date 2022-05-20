from enum import Enum
from pydantic import BaseModel, Field
from bson import ObjectId

class LanguageEnum(str, Enum):
    de = 'de'
    en = 'en'


class UserSettingsSchema(BaseModel):
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

# create response model for the get endpoint
class UserSettingsResponse(BaseModel):
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
