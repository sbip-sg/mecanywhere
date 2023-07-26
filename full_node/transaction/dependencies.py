from functools import lru_cache
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import aiohttp
import redis
from contract import PaymentContract
from config import Config
from common.middleware.credential_authentication import (
    CredentialAuthenticationMiddleware,
)
from contract import PaymentContract
from services.task_service import TaskService


@lru_cache()
def get_config() -> Config:
    return Config("../config.json", "config.json")


async def get_session() -> aiohttp.ClientSession:
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
    session: aiohttp.ClientSession = Depends(get_session),
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


async def has_ca_access(
    ca_middleware: CredentialAuthenticationMiddleware = Depends(get_ca_middleware),
    authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> bool:
    await ca_middleware.has_access(authorization)


def get_contract_instance(config: Config = Depends(get_config)) -> PaymentContract:
    return PaymentContract(config)


def get_task_service(
    config: Config = Depends(get_config),
    contract: PaymentContract = Depends(get_contract_instance),
) -> TaskService:
    return TaskService(config, contract)
