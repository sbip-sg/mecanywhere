from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    username: str
    did: str

class CreateVcResponse(BaseModel):
    result: dict
