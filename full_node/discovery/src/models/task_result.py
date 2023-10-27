from pydantic import BaseModel, Field


class TaskResultModel(BaseModel):
    id: str = Field(..., example="001")
    content: str = Field(..., example="Hello World")
    resource_consumed: float = Field(..., example=0.1)
    transaction_start_datetime: int = Field(..., example=1694563200)
    transaction_end_datetime: int = Field(..., example=1694649600)
    duration: int = Field(..., example=1)
