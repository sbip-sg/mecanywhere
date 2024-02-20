from functools import lru_cache
import aiohttp
import redis
from aiohttp import ClientSession
from config import Config
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from common.middleware.credential_authentication import (
    CredentialAuthenticationMiddleware,
)
from contracts.scheduler_contract import SchedulerContract
from contracts.tower_contract import TowerContract
from services.cache import DCache
from services.offloading_service import OffloadingService
from services.message_queue.task_publisher import BasicTaskPublisher
from services.transaction_service import TransactionService


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


def get_ca_middleware(
    config: Config = Depends(get_config),
    session: ClientSession = Depends(get_session),
    redis: redis.Redis = Depends(get_redis_client),
) -> CredentialAuthenticationMiddleware:
    return CredentialAuthenticationMiddleware(config, session, redis)


def get_did_from_token(
    ca_middleware: CredentialAuthenticationMiddleware = Depends(get_ca_middleware),
    authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> str:
    return ca_middleware.get_did_from_token(authorization)


def get_po_did_from_token(
    ca_middleware: CredentialAuthenticationMiddleware = Depends(get_ca_middleware),
    authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> str:
    return ca_middleware.get_po_did_from_token(authorization)


def get_token(
    ca_middleware: CredentialAuthenticationMiddleware = Depends(get_ca_middleware),
    authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> str:
    return ca_middleware.get_token(authorization)


async def has_ca_access(
    ca_middleware: CredentialAuthenticationMiddleware = Depends(get_ca_middleware),
    authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> bool:
    await ca_middleware.has_access(authorization)


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
    config: Config = Depends(get_config),
) -> OffloadingService:
    return OffloadingService(
        contract,
        publisher,
        cache,
        config.get_server_host_name(),
        config.get_server_host_did(),
        config.get_server_host_po_did(),
    )


def get_transaction_service(
    config: Config = Depends(get_config),
    session: ClientSession = Depends(get_session),
) -> TransactionService:
    return TransactionService(config, session)
