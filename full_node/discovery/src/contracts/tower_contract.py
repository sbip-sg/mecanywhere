from contracts.contract import Contract
from config import Config

class TowerContract(Contract):
    def __init__(self, config: Config):
        super().__init__(config, config.get_tower_abi_path(), config.get_tower_contract_addr())

    def registerTower(self, size_limit: int, public_connection: str, fee: int, fee_type: int):
        unbuilt_function = self.contract.functions.registerAsTower(size_limit, public_connection, fee, fee_type)
        stake =  self.w3.to_wei(10, "ether")
        self.call_function(unbuilt_function, {"gas": 750000, "value": stake})

    def deleteTower(self, tower_address: str):
        unbuilt_function = self.contract.functions.deleteTower(tower_address)
        self.call_function(unbuilt_function, {"gas": 750000})

    def acceptHost(self, host_address: str):
        unbuilt_function = self.contract.functions.acceptHost(host_address)
        self.call_function(unbuilt_function, {"gas": 750000})

    def deleteHost(self, host_address: str):
        unbuilt_function = self.contract.functions.deleteHost(host_address)
        self.call_function(unbuilt_function, {"gas": 750000})
