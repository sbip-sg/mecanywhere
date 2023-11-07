from pydantic import BaseModel, Field

from models.did import DIDModel
from models.db_schema import UserDetails


class ClaimData(DIDModel, UserDetails):
    # instantiate with variable number of keyword args or all positional args
    def __init__(self, *args, **kwargs):
        if len(kwargs) > 0:
            super().__init__(**kwargs)
            return
        fields = ["did", "name", "gender", "age"]
        kwargs = dict(zip(fields, args))
        super().__init__(**kwargs)


class NameSchema(BaseModel):
    type: str = Field(..., example="string")
    description: str = Field(..., example="the name of the certificate owner")


class GenderSchema(BaseModel):
    enum: list = Field(..., example=["M", "F"])
    type: str = Field(..., example="string")
    description: str = Field(..., example="the gender of the certificate owner")


class AgeSchema(BaseModel):
    type: str = Field(..., example="integer")
    description: str = Field(..., example="the age of the certificate owner")


class ClaimPropertiesSchema(BaseModel):
    name: NameSchema
    gender: GenderSchema
    age: AgeSchema


class ClaimSchema(BaseModel):
    title: str = Field(..., example="schema_title")
    description: str = Field(..., example="schema_description")
    properties: ClaimPropertiesSchema
    required: list = Field(..., example='["name", "age"]')
