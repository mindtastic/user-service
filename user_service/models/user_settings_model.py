from enum import Enum
from pydantic import UUID4, BaseModel, Field
from bson import ObjectId
from typing import Optional

class LanguageEnum(str, Enum):
    de = 'de'
    en = 'en'


class UserSettingsSchema(BaseModel):
    user_id: Optional[UUID4]
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
