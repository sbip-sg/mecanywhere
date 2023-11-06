from pydantic import Field

from models.did import DIDModel


class AccountModel(DIDModel):
    username: str = Field(..., example="username")
    password: str = Field(..., example="password")
