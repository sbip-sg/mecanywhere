from pydantic import BaseModel, Field


class Transaction(BaseModel):
    id: int
    transaction_id: str
    did: str
    resource_consumed: int
    transaction_start_datetime: int
    transaction_end_datetime: int
    task_name: str
    duration: int
    price: float
    po_did: str
    host_did: str
    host_po_did: str
    network_reliability: int

    def __init__(self, *args):
        fields = [
            "id",
            "transaction_id",
            "did",
            "resource_consumed",
            "transaction_start_datetime",
            "transaction_end_datetime",
            "task_name",
            "duration",
            "price",
            "po_did",
            "host_did",
            "host_po_did",
            "network_reliability",
        ]
        kwargs = dict(zip(fields, args))
        super().__init__(**kwargs)