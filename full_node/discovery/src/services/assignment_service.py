from contract import DiscoveryContract
from common import get_current_timestamp


class AssignmentService(object):
    def __init__(self, contract: DiscoveryContract) -> None:
        self.contract = contract

    def assign(self, did: str) -> str:
        return self.contract.get_user_queue(get_current_timestamp())

    def remove(self) -> None:
        pass
