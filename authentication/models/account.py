from pydantic import BaseModel, Field


class AccountModel(BaseModel):
    did: str = Field(..., example="did:meca:0xfd340b5a30de452ae4a14dd1b92a7006868a29c8")
    username: str = Field(..., example="username")
    password: str = Field(..., example="password")
