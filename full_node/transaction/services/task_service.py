from config import Config
from contract import PaymentContract
from exceptions.http_exceptions import ContractException
from models.task_metadata import Resources, TaskMetadataInput


class TaskService:
    def __init__(self, config: Config, contract: PaymentContract):
        self.config = config
        self.contract = contract

    def process_task(self, client_po_did: str, host_po_did: str, task_metadata: TaskMetadataInput):
        resource_consumed = task_metadata.resource_consumed
        fee = self._calculate_fee(resource_consumed)
        if fee == 0:
            return 0
        try:
            self.contract.increase_balance(host_po_did, fee)
            self.contract.decrease_balance(client_po_did, fee)
        except Exception as e:
            raise ContractException(f"Error: Failed to change balance in payment contract. {str(e)}")
        return fee

    def _calculate_fee(self, resource_consumed: Resources):
        if resource_consumed is None:
            return 0
        resource_cpu = resource_consumed.cpu
        resource_memory = resource_consumed.memory
        return resource_cpu * resource_memory * 0.1
    
