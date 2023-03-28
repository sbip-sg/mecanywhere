from contract import DiscoveryContract
from common import get_current_timestamp


class MonitoringService(object):
    def __init__(self, contract: DiscoveryContract) -> None:
        self.contract = contract

    def heartbeat(self, ip_address: str) -> None:
        self.contract.set_ip_address_timestamp(ip_address, get_current_timestamp())
