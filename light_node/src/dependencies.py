from main import _result_mapping, _compute_task, _heartbeat_task, _registered_as_host, _registered_as_user, session, config
from models.result import ResultMapping
from tasks.compute_task import ComputeTask
from tasks.heartbeat_task import HeartbeatTask
from config import Config
import aiohttp


async def get_result_mapping() -> ResultMapping:
    return _result_mapping

async def get_compute_task() -> ComputeTask:
    return _compute_task

async def get_heartbeat_task() -> HeartbeatTask:
    return _heartbeat_task

async def get_registered_as_host():
    return _registered_as_host

async def get_registered_as_user():
    return _registered_as_user

async def get_session() -> aiohttp.ClientSession:
    return session

async def get_config() -> Config:
    return config