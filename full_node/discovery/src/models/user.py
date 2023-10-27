from pydantic import BaseModel, Field

class User(BaseModel):
    did: str = Field(None)
    po_did: str = Field(None)
    index: int = Field(None)
    is_user: bool = Field(None)
    timestamp: int = Field(None)
    latency: int = Field(None)
    queue: str = Field(None)

    def __init__(self, *args, **kwargs):
        fields = [
            "did",
            "po_did",
            "index",
            "is_user",
            "timestamp",
            "latency",
            "queue",
        ]
        kwargs = dict(zip(fields, args))
        super().__init__(**kwargs)
