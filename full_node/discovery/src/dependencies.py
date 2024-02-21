from functools import lru_cache
import aiohttp
import redis
from aiohttp import ClientSession
from config import Config
from fastapi import Depends
from contracts.scheduler_contract import SchedulerContract
from contracts.tower_contract import TowerContract
from services.cache import DCache
from services.offloading_service import OffloadingService
from services.message_queue.task_publisher import BasicTaskPublisher


@lru_cache()
def get_config() -> Config:
    return Config("../config.json", "../../config.json")


async def get_session() -> ClientSession:
    async with aiohttp.ClientSession() as session:
        yield session


def get_cache(config: Config = Depends(get_config)) -> DCache:
    return DCache(config)


def get_redis_client(config: Config = Depends(get_config)) -> redis.Redis:
    return redis.Redis(
        host=config.get_redis_host(),
        port=config.get_redis_port(),
        decode_responses=True,
    )


def get_rpc_task_publisher(config: Config = Depends(get_config)) -> BasicTaskPublisher:
    return BasicTaskPublisher(config.get_mq_url())


def get_tower_contract(config: Config = Depends(get_config)) -> TowerContract:
    return TowerContract(config)


def get_scheduler_contract(config: Config = Depends(get_config)) -> SchedulerContract:
    return SchedulerContract(config)


def get_offloading_service(
    contract: SchedulerContract = Depends(get_scheduler_contract),
    publisher: BasicTaskPublisher = Depends(get_rpc_task_publisher),
    cache: DCache = Depends(get_cache),
) -> OffloadingService:
    return OffloadingService(
        contract,
        publisher,
        cache
    )
