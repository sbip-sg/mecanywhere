from pydantic import BaseModel, Field

from models.task_result import TaskResultModel


class AuthenticationResponse(BaseModel):
    access_token: str = Field(description="JWT format token")
    access_token_type: str = Field(example="Bearer")
    refresh_token: str = Field(description="JWT format token")
    refresh_token_type: str = Field(example="Bearer")


class PublishTaskResponse(BaseModel):
    status: int = Field(..., example=1)
    transaction_id: str = Field(..., example="001")
    task_result: TaskResultModel = Field(None)
    host_did: str = Field(None)
    network_reliability: int = Field(..., example=100)
    error: str = Field(None, example="")


class OffloadResponse(BaseModel):
    transaction_id: str = Field(..., example="001")
    task_id: str = Field(..., example="001")
    status: int = Field(..., example=1)
    response: str = Field(..., example="Hello World")
    error: str = Field(None, example="")
