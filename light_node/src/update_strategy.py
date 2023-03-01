from abc import ABC, abstractmethod
import aiohttp
from typing import Dict


class UpdateStrategy(ABC):
    @abstractmethod
    async def update(self, data: Dict):
        pass


class HttpReqUpdateStrategy(UpdateStrategy):
    def __init__(self, url) -> None:
        self.url = url

    async def update(self, data: Dict):
        async with aiohttp.ClientSession() as session:
            await session.post(self.url, json=data)
