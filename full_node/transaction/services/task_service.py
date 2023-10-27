from config import Config
from contract import PaymentContract
from models.task_metadata_input import TaskMetadataInput


class TaskService:
    def __init__(self, config: Config, contract: PaymentContract):
        self.config = config
        self.contract = contract

    def process_task(self, client_po_did: str, host_po_did: str, task_metadata: TaskMetadataInput):
        fee = self._calculate_fee(task_metadata)
        self.contract.increase_balance(host_po_did, fee)
        self.contract.decrease_balance(client_po_did, fee)
        return fee

    def _calculate_fee(self, task_metadata: TaskMetadataInput):
        return task_metadata.resource_consumed * 0.1
    
