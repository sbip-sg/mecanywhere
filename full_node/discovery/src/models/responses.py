from pydantic import BaseModel, Field


class RegistrationResponse(BaseModel):
    access_token: str = Field(description="JWT format token")
    token_type: str = Field(example="bearer")


class AssignmentResponse(BaseModel):
    queue: str
