from contract import DiscoveryContract
from services.strategies.ip_assign_strategy import RoundRobinAssignStrategy


class AssignmentService(object):
    def __init__(self, contract: DiscoveryContract) -> None:
        self.contract = contract
        self.strategy = RoundRobinAssignStrategy(self.contract)

    def assign(self) -> str:
        return self.strategy.assign()

    def remove(self, ip: str) -> None:
        self.strategy.remove(ip)
