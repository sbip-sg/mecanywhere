from pydantic import BaseModel, Field


class RegistrationResponse(BaseModel):
    access_token: str = Field(description="JWT format token")
    access_token_type: str = Field(example="Bearer")
    refresh_token: str = Field(description="JWT format token")
    refresh_token_type: str = Field(example="Bearer")


class TaskResultModel(BaseModel):
    id: str = Field(..., example="001")
    content: str = Field(..., example="Hello World")
    resource_consumed: float = Field(..., example=0.1)
    transaction_start_datetime: int = Field(..., example=1694563200)
    transaction_end_datetime: int = Field(..., example=1694649600)
    duration: int = Field(..., example=1)


class PublishTaskResponse(BaseModel):
    status: int = Field(..., example=1)
    transaction_id: str = Field(..., example="001")
    task_result: TaskResultModel = Field(None)
    network_reliability: int = Field(..., example=100)
    error: str = Field(None, example="")


class OffloadResponse(BaseModel):
    task_id: str = Field(..., example="001")
    status: int = Field(..., example=1)
    response: str = Field(..., example="Hello World")
    error: str = Field(None, example="")
