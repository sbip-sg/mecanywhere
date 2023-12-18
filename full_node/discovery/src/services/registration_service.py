from contract import DiscoveryContract
from utils import get_current_timestamp


class RegistrationService(object):
    def __init__(self, contract: DiscoveryContract) -> None:
        self.contract = contract

    def is_registered(self, did: str) -> bool:
        return self.contract.get_user(did).is_user

    def register_host(self, did: str, po_did: str, cpu: int, mem: int) -> None:
        self.contract.set_user(did, po_did, get_current_timestamp(), cpu, mem)

    def deregister_host(self, did: str) -> None:
        self.contract.remove_user(did)

    def register_client(self, did: str) -> None:
        pass

    def deregister_client(self, did: str) -> None:
        pass
    