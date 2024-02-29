from contracts.contract import Contract
from config import Config

class TowerContract(Contract):
    def __init__(self, config: Config):
        super().__init__(config, config.get_tower_abi_path(), config.get_tower_contract_addr())

    def registerTower(self, size_limit: int, public_connection: str, fee: int, fee_type: int, stake: int):
        unbuilt_function = self.contract.functions.registerAsTower(
            sizeLimit=size_limit,
            publicConnection=public_connection,
            fee=fee,
            feeType=fee_type)
        stake_wei =  self.w3.to_wei(stake, "ether")
        self.call_function(unbuilt_function, {"value": stake_wei})

    def deleteTower(self):
        unbuilt_function = self.contract.functions.deleteTower()
        self.call_function(unbuilt_function)

    def acceptHost(self, host_address: str):
        unbuilt_function = self.contract.functions.acceptHost(host_address)
        self.call_function(unbuilt_function)

    def deleteHost(self, host_address: str):
        unbuilt_function = self.contract.functions.deleteHost(host_address)
        self.call_function(unbuilt_function)
