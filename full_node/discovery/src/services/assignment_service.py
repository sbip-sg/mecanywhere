from contract import DiscoveryContract
from utils import get_current_timestamp


class AssignmentService(object):
    def __init__(self, contract: DiscoveryContract) -> None:
        self.contract = contract

    def assign(self, did: str) -> str:
        print("pydid", did)
        return self.contract.get_user_queue(get_current_timestamp())

    def remove(self) -> None:
        pass
