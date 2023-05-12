from contract import DiscoveryContract
from common import get_current_timestamp


class MonitoringService(object):
    def __init__(self, contract: DiscoveryContract) -> None:
        self.contract = contract

    def heartbeat(self, did: str) -> None:
        self.contract.set_user(did, get_current_timestamp(), 0)
