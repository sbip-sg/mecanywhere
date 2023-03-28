from pydantic import BaseModel


class ComputeRequest(BaseModel):
    id: str
    binary: str


class ComputeResultRequest(BaseModel):
    id: str


class UpdateResultRequest(BaseModel):
    id: str
    result: str
