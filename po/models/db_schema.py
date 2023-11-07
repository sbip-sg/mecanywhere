from pydantic import Field, BaseModel


class AccountModel(BaseModel):
    username: str = Field(..., example="username")
    password: str = Field(..., example="password")


class UserDetails(BaseModel):
    name: str = Field(None, example="John Doe")
    gender: str = Field(None, example="M")
    age: int = Field(None, example=42)
