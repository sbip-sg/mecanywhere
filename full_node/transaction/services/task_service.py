from config import Config
from contract import PaymentContract
from models.task_metadata_input import TaskMetadataInput


class TaskService:
    def __init__(self, config: Config, contract: PaymentContract):
        self.config = config
        self.contract = contract

    def process_task(self, client_po_did: str, host_po_did: str, task_metadata: TaskMetadataInput):
        resource_consumed = task_metadata.resource_consumed
        if resource_consumed is None or resource_consumed == 0:
            return 0
        fee = self._calculate_fee(resource_consumed)
        self.contract.increase_balance(host_po_did, fee)
        self.contract.decrease_balance(client_po_did, fee)
        return fee

    def _calculate_fee(self, resource_consumed: float):
        return resource_consumed * 0.1
    
