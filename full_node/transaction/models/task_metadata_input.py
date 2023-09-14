from pydantic import BaseModel, Field


class TaskMetadataInput(BaseModel):
    session_id: str = Field(..., example='0001')
    resource_consumed: float = Field(..., example=0.1)
    session_start_datetime: int = Field(..., example=1694563200)
    session_end_datetime: int = Field(..., example=1694649600)
    task: str = Field(..., example='task1')
    duration: int = Field(..., example=100)
    network_reliability: int = Field(..., example=100)
