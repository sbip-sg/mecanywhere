from pydantic import BaseModel


class UserResponse(BaseModel):
    username: str
    did: str


class IssuerResponse(BaseModel):
    result: dict | None
    errorCode: int
    errorMessage: str
    transactionInfo: dict | None
