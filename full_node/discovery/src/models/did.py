from pydantic import BaseModel, Field


class DIDModel(BaseModel):
    did: str = Field(
        ...,
        example="did:bdsv:0x0fa21fd3d11d2cd5e6cdef2c7cd6531a25a5964f",
    )
