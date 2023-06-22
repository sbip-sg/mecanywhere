from pydantic import BaseModel, Field


class WithdrawalRequest(BaseModel):
    did: str = Field(
        ...,
        example="did:meca:0x0fa21fd3d11d2cd5e6cdef2c7cd6531a25a5964f",
    )
    address: str = Field(
        ...,
        example="0x0fa21fd3d11d2cd5e6cdef2c7cd6531a25a5964f",
    )
    amount: str = Field(
        ...,
        example=0.001,
        description="Amount in ether. Provide as string for accuracy.",
    )
