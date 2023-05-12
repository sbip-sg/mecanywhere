from pydantic import BaseModel, Field


class DIDModel(BaseModel):
    did: str = Field(
        ...,
        example="did:bdsv:0x52c328ef8b382b1d71cc262b868d803a137ab8d8",
    )
