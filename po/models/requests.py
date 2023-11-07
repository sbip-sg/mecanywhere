from pydantic import BaseModel
from models.db_schema import AccountModel, UserDetails


class CreateAccountRequest(AccountModel, UserDetails):
    pass


class CreateUserRequest(BaseModel):
    public_key: str
    account: AccountModel
