from enum import Enum
import uuid
from pydantic import BaseModel, Field
from bson import ObjectId

class LanguageEnum(str, Enum):
    de = 'de'
    en = 'en'


class UserSettingsSchema(BaseModel):
    user_id : uuid = Field(...)
    language: LanguageEnum = LanguageEnum.de #Default value is "de"
    #TODO more settings to be added here

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "userId": "123e4567-e89b-12d3-a456-426655440000",
                "language": "de"
            }
        }

# create response model for the get endpoint
class UserSettingsResponse(BaseModel):
    language: LanguageEnum = LanguageEnum.de #Default value is "de"
    #TODO more settings to be added here

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "language": "de"
            }
        }
