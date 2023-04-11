from contract import DiscoveryContract
from common import get_current_timestamp


class RegistrationService(object):
    def __init__(self, contract: DiscoveryContract) -> None:
        self.contract = contract

    def register_host(self, ip_address: str) -> None:
        self.contract.set_ip_address_timestamp(ip_address, get_current_timestamp())

    def deregister_host(self, ip_address: str) -> None:
        self.contract.removeIpAddress(ip_address)

    def register_user(self, ip_address: str) -> None:
        pass

    def deregister_user(self, ip_address: str) -> None:
        pass
    