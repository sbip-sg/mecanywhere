from models.result import InMemoryResultMapping, ResultMapping
from models.message import ComputeRequest
from tasks.compute_task import ComputeTask
from tasks.heartbeat_task import HeartbeatTask
from config import Config
import aiohttp


class Host:
    def __init__(self, config: Config, session: aiohttp.ClientSession):
        self.result_mapping: ResultMapping = InMemoryResultMapping()
        self.compute_task: ComputeTask = ComputeTask(result_mapping=self.result_mapping)
        self.heartbeat_task: HeartbeatTask = HeartbeatTask(
            url=config.get_heartbeat_url(),
            periodic_interval=config.get_heartbeat_interval_sec(),
            session=session,
        )
        print(self)

    async def start(self):
        self.compute_task.start()
        await self.heartbeat_task.start()

    def stop(self):
        print(self)
        self.compute_task.terminate()
        self.heartbeat_task.terminate()

    def get_result(self, id: str) -> ResultMapping:
        return self.result_mapping.get(id)
    
    def compute(self, compute_request: ComputeRequest):
        self.compute_task.enqueue(compute_request)


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

    def get_result(self, id: str) -> ResultMapping:
        return self.host.get_result(id)
    
    def compute(self, compute_request: ComputeRequest):
        self.host.compute(compute_request)
    