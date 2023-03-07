import asyncio
from contract import DiscoveryContract
from ip_assign_strategy import IpAssignStrategy
from common import get_current_timestamp


class CleanupTask:
    def __init__(self, interval_in_sec: int, expire_in_sec: int, contract: DiscoveryContract, ip_assigner) -> None:
        self.interval = interval_in_sec
        self.expire = expire_in_sec
        self.contract = contract
        self.ip_assigner = ip_assigner

    def run(self):
        asyncio.create_task(self._loop())

    async def _loop(self):
        while True:
            try:
                await asyncio.sleep(self.interval)
                ip_timestamps_list = self.contract.getAllIpAddressTimestamps()
                for ip, timestamp in ip_timestamps_list:
                    if (self.expire < get_current_timestamp() - timestamp):
                        self.contract.removeIpAddress(ip)
                        self.ip_assigner.remove(ip)
            except:
                pass
