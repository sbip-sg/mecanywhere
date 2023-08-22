from pydantic import BaseModel, Field

class DidRecord(BaseModel):
    id: str
    did: str
    resource_consumed: float
    session_start_datetime: int
    session_end_datetime: int
    task: str
    duration: int
    price: float

    class Config:
        orm_mode = True
