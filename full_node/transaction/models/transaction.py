from models.task_metadata import DatabaseTaskMetadata


class Transaction(DatabaseTaskMetadata):
    id: int
    did: str
    price: float
    po_did: str
    host_did: str
    host_po_did: str

    def __init__(self, *args):
        fields = [
            "id",
            "transaction_id",
            "did",
            "resource_cpu",
            "resource_memory",
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