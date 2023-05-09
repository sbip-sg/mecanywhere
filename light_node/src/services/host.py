from tasks.compute_task import ComputeTask
from tasks.heartbeat_task import HeartbeatTask
from config import Config
import aiohttp


class Host:
    def __init__(self, config: Config, session: aiohttp.ClientSession):
        self.compute_task: ComputeTask = ComputeTask()
        self.heartbeat_task: HeartbeatTask = HeartbeatTask(
            url=config.get_heartbeat_url(),
            periodic_interval=config.get_heartbeat_interval_sec(),
            session=session,
        )

    async def start(self):
        self.compute_task.start()
        await self.heartbeat_task.start()

    def stop(self):
        self.compute_task.terminate()
        self.heartbeat_task.terminate()


class HostRegistrationService:
    def __init__(self, config: Config, session: aiohttp.ClientSession):
        self.host = Host(config, session)
        self.registered = False

    async def start_hosting(self):
        await self.host.start()

    def stop_hosting(self):
        self.host.stop()

    def is_registered(self) -> bool:
        return self.registered

    def set_is_registered(self, value: bool):
        self.registered = value
