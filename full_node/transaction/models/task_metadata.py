from pydantic import BaseModel, Field, validator


class Resources(BaseModel):
    cpu: int = Field(default=0, example=2, ge=0)
    memory: int = Field(default=0, example=256, ge=0)


class TaskMetadataInput(BaseModel):
    transaction_id: str = Field(
        default="0", example="0001", min_length=1, max_length=255
    )
    resource_consumed: Resources = Field(...)
    transaction_start_datetime: int = Field(default=0, example=1694563200, ge=0)
    transaction_end_datetime: int = Field(default=0, example=1694649600, ge=0)
    task_name: str = Field(default="", example="task1", min_length=1, max_length=255)
    duration: int = Field(default=0, example=100, ge=0)
    network_reliability: int = Field(default=0, example=100, ge=0, le=100)

    @validator("transaction_end_datetime")
    def validate_transaction_end_datetime(cls, value, values):
        if (
            "transaction_start_datetime" in values
            and value < values["transaction_start_datetime"]
        ):
            raise ValueError(
                "Transaction end datetime must be greater than or equal to the start datetime"
            )
        return value


class DatabaseTaskMetadata(BaseModel):
    transaction_id: str = Field(
        default="0", example="0001", min_length=1, max_length=255
    )
    resource_cpu: int = Field(default=0, example=2, ge=0)
    resource_memory: int = Field(default=0, example=256, ge=0)
    transaction_start_datetime: int = Field(default=0, example=1694563200, ge=0)
    transaction_end_datetime: int = Field(default=0, example=1694649600, ge=0)
    task_name: str = Field(default="", example="task1", min_length=1, max_length=255)
    duration: int = Field(default=0, example=100, ge=0)
    network_reliability: int = Field(default=0, example=100, ge=0, le=100)
