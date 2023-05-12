from contract import DiscoveryContract


class AssignmentService(object):
    def __init__(self, contract: DiscoveryContract) -> None:
        self.contract = contract

    def assign(self, did: str) -> str:
        return self.contract.get_user_queue()

    def remove(self) -> None:
        pass
