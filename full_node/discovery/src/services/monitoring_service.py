from contract import DiscoveryContract
from utils import get_current_timestamp


class MonitoringService(object):
    def __init__(self, contract: DiscoveryContract) -> None:
        self.contract = contract

    def is_registered(self, did: str) -> bool:
        return self.contract.get_user(did).is_user

    def heartbeat(self, did: str) -> None:
        self.contract.update_timestamp(did, get_current_timestamp())
