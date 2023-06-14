from pydantic import BaseModel, Field


class DIDModel(BaseModel):
    did: str = Field(
        ...,
        example="did:meca:0x0fa21fd3d11d2cd5e6cdef2c7cd6531a25a5964f",
    )
