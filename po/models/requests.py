from pydantic import BaseModel
from models.account import AccountModel


class CreateAccountRequest(AccountModel):
    pass


class CreateDidRequest(BaseModel):
    public_key: str


class CreateVcRequest(AccountModel):
    pass
