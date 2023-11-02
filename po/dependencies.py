from functools import lru_cache
from fastapi import Depends
import aiohttp
from config import Config
from services.account_service import AccountService
from services.database import Database
from services.issuer_service import IssuerService


async def get_client_session():
    async with aiohttp.ClientSession() as session:
        yield session


@lru_cache()
def get_config():
    return Config("config.json")


def get_database(config: Config = Depends(get_config)):
    return Database(config)


def get_account_service(database: Database = Depends(get_database)):
    return AccountService(database)


def get_issuer_service(
    config: Config = Depends(get_config),
    session: aiohttp.ClientSession = Depends(get_client_session),
):
    return IssuerService(config, session)
