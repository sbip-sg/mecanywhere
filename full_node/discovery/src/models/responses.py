from pydantic import BaseModel, Field


class RegistrationResponse(BaseModel):
    access_token: str = Field(description="JWT format token")
    access_token_type: str = Field(example="Bearer")
    refresh_token: str = Field(description="JWT format token")
    refresh_token_type: str = Field(example="Bearer")


class PublishTaskResponse(BaseModel):
    status: int = Field(..., example=1)
    response: str = Field(..., example="Hello World")
    error: str = Field(None, example="")


class OffloadResponse(PublishTaskResponse):
    task_id: str = Field(..., example="001")
