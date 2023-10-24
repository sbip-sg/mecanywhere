from pydantic import BaseModel, Field


class TaskMetadataInput(BaseModel):
    transaction_id: str = Field(..., example='0001')
    resource_consumed: float = Field(..., example=0.1)
    transaction_start_datetime: int = Field(..., example=1694563200)
    transaction_end_datetime: int = Field(..., example=1694649600)
    task_name: str = Field(..., example='task1')
    duration: int = Field(..., example=100)
    network_reliability: int = Field(..., example=100)
