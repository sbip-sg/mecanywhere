from contract import DiscoveryContract
from utils import get_current_timestamp


class RegistrationService(object):
    def __init__(self, contract: DiscoveryContract) -> None:
        self.contract = contract

    def register_host(self, did: str) -> None:
        self.contract.set_user(did, get_current_timestamp(), 0)

    def deregister_host(self, did: str) -> None:
        self.contract.remove_user(did)

    def register_client(self, did: str) -> None:
        pass

    def deregister_client(self, did: str) -> None:
        pass
    