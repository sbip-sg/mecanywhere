from pydantic import BaseModel, Field

class ClaimData(BaseModel):
    did: str = Field(..., example="did:meca:0xfd340b5a30de452ae4a14dd1b92a7006868a29c8")
    name: str = Field(..., example="John Doe")
    age: int = Field(..., example=42)
