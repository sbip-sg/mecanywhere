from pydantic import BaseModel, Field


class ClaimData(BaseModel):
    did: str = Field(..., example="did:meca:0xfd340b5a30de452ae4a14dd1b92a7006868a29c8")
    name: str = Field(None, example="John Doe")
    gender: str = Field(None, example="M")
    age: int = Field(None, example=42)

    # instantiate with variable number of keyword args or all positional args
    def __init__(self, *args, **kwargs):
        if len(kwargs) > 0:
            super().__init__(**kwargs)
            return
        fields = [
            "did",
            "name",
            "gender",
            "age"
        ]
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
