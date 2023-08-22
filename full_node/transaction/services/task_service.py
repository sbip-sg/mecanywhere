from fastapi import Depends
from config import Config
from contract import PaymentContract


class TaskService:
    def __init__(self, config: Config, contract: PaymentContract):
        self.config = config
        self.contract = contract

    def process_task(self, task_type, po_did, task_id, task_metadata):
        # TODO: record task and match with other party
        # store where?
        # what metadata to record?

        fee = self._calculate_after_agent_fee(task_metadata)
        if task_type == "client":
            self.contract.decrease_balance(po_did, fee)
        else:
            self.contract.increase_balance(po_did, fee)
        return fee

    def _calculate_after_agent_fee(self, task_metadata):
        return 0
    
