from abc import ABC, abstractmethod
from contract import DiscoveryContract


class IpAssignStrategy(ABC):
    @abstractmethod
    def assign(self) -> str:
        pass

    @abstractmethod
    def remove(self, ip: str) -> None:
        pass


class RoundRobinAssignStrategy(IpAssignStrategy):
    def __init__(self, contract: DiscoveryContract) -> None:
        self.ip_timestamp_list = contract.getAllIpAddressTimestamps()
        self.contract = contract

    def assign(self) -> str:
        if len(self.ip_timestamp_list) == 0:
            self.ip_timestamp_list = self.contract.getAllIpAddressTimestamps()

        ip = self.ip_timestamp_list.pop()[0]

        return ip

    def remove(self, ip: str) -> None:
        try:
            self.ip_timestamp_list.remove(ip)
        except:
            pass
