from models.task_metadata import DatabaseTaskMetadata

class DidRecord(DatabaseTaskMetadata):
    price: float

    class Config:
        orm_mode = True


class PoDidRecord(DatabaseTaskMetadata):
    price: float
    did: str
    po_did: str
    host_did: str
    host_po_did: str

    class Config:
        orm_mode = True
