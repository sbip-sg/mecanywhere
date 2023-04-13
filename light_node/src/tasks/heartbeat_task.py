from aiohttp import ClientSession
import asyncio


class HeartbeatTask:
    def __init__(self, url, periodic_interval, session: ClientSession) -> None:
        self.url = url
        self.periodic_interval = periodic_interval
        self.session = session
        self._loop_running = asyncio.Event()
        self._loop_running.set()

    async def start(self):
        asyncio.ensure_future(self._run())

    async def _run(self):
        while self._loop_running.is_set():
            try:
                async with self.session.post(self.url, json={}):
                    pass
            except Exception as e:
                print(e)

            await asyncio.sleep(self.periodic_interval)

    def terminate(self) -> None:
        self._loop_running.clear()
