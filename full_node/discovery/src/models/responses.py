from pydantic import BaseModel, Field


class RegistrationResponse(BaseModel):
    access_token: str = Field(description="JWT format token")
    access_token_type: str = Field(example="bearer")
    refresh_token: str = Field(description="JWT format token")
    refresh_token_type: str = Field(example="bearer")

class AssignmentResponse(BaseModel):
    queue: str
