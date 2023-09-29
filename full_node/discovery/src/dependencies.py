from functools import lru_cache
import aiohttp
import redis
from aiohttp import ClientSession
from config import Config
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from contract import DiscoveryContract
from common.middleware.credential_authentication import (
    CredentialAuthenticationMiddleware,
)
from services.offloading_service import OffloadingService
from services.registration_service import RegistrationService
from services.monitoring_service import MonitoringService
from services.account_creation_service import AccountCreationService
from services.login_service import LoginService
from services.task_publisher import RPCTaskPublisher, BasicTaskPublisher


@lru_cache()
def get_config() -> Config:
    return Config("../config.json", "../../config.json")


async def get_session() -> ClientSession:
    async with aiohttp.ClientSession() as session:
        yield session


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


async def has_ca_access(
    ca_middleware: CredentialAuthenticationMiddleware = Depends(get_ca_middleware),
    authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> bool:
    await ca_middleware.has_access(authorization)


def get_discovery_contract(config: Config = Depends(get_config)) -> DiscoveryContract:
    return DiscoveryContract(config)


def get_account_creation_service(
    config: Config = Depends(get_config),
) -> AccountCreationService:
    return AccountCreationService(config)


def get_login_service() -> LoginService:
    return LoginService()


def get_rpc_task_publisher(config: Config = Depends(get_config)) -> RPCTaskPublisher:
    return RPCTaskPublisher(config)


def get_basic_task_publisher(
    config: Config = Depends(get_config),
) -> BasicTaskPublisher:
    return BasicTaskPublisher(config)


def get_offloading_service(
    contract: DiscoveryContract = Depends(get_discovery_contract),
    rpc_publisher: RPCTaskPublisher = Depends(get_rpc_task_publisher),
    basic_publisher: BasicTaskPublisher = Depends(get_basic_task_publisher),
    cache: redis.Redis = Depends(get_redis_client),
) -> OffloadingService:
    return OffloadingService(contract, rpc_publisher, basic_publisher, cache)


def get_registration_service(
    contract: DiscoveryContract = Depends(get_discovery_contract),
) -> RegistrationService:
    return RegistrationService(contract)


def get_monitoring_service(
    contract: DiscoveryContract = Depends(get_discovery_contract),
) -> MonitoringService:
    return MonitoringService(contract)
