from pydantic import BaseModel, Field

class DidRecord(BaseModel):
    id: str
    did: str
    resource_consumed: int
    session_start_datetime: int
    session_end_datetime: int
    task: str
    duration: int
    price: float
    po_did: str
    network_reliability: int

    class Config:
        orm_mode = True
