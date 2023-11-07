from pydantic import BaseModel


class UserResponse(BaseModel):
    username: str


class DidServiceResponse(BaseModel):
    result: dict | None
    errorCode: int
    errorMessage: str
    transactionInfo: dict | None


class CreateUserResponse(BaseModel):
    did: str
    credential: dict
