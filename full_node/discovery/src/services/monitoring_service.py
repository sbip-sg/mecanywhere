from contract import DiscoveryContract
from utils import get_current_timestamp


class MonitoringService(object):
    def __init__(self, contract: DiscoveryContract) -> None:
        self.contract = contract

    def heartbeat(self, did: str, po_did: str) -> None:
        # TODO: check if registered
        self.contract.set_user(did, po_did, get_current_timestamp(), 0)
