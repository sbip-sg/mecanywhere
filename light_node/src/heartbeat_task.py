import aiohttp
import asyncio


class HeartbeatTask:
    def __init__(self, url, periodic_interval) -> None:
        self.url = url
        self.periodic_interval = periodic_interval

    def start(self):
        asyncio.create_task(self._run())

    async def _run(self):
        headers={"Authorization": ""} #TODO
        session = aiohttp.ClientSession(headers=headers)
        while True:
            try:
                async with session.post(self.url, json={}):
                    pass
            except Exception as e:
                print(e)

            await asyncio.sleep(self.periodic_interval)
