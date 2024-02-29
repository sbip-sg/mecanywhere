from contracts.contract import Contract
from config import Config

class SchedulerContract(Contract):
    def __init__(self, config: Config):
        super().__init__(config, config.get_scheduler_abi_path(), config.get_scheduler_contract_addr())

    def send_task(self, tower_address: str, host_address: str, task_hash: str, caller_host_fee: int, input_size: int, input_hash: bytes):
        unbuilt_function = self.contract.functions.sendTask(tower_address, host_address, task_hash, caller_host_fee, input_size, input_hash)
        self.call_function(unbuilt_function)
    
    def get_running_task(self, task_id: str):
        task_tuple = self.contract.functions.getRunningTask(task_id).call()
        return task_tuple
    
    def finish_task(self, task_id: bytes):
        unbuilt_function = self.contract.functions.finishTask(task_id)
        self.call_function(unbuilt_function)
