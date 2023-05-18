from fastapi import Depends
from config import Config
from services.account_service import AccountService
from services.database import Database


def get_config():
    return Config("config.json")


def get_database(config: Config = Depends(get_config)):
    return Database(config)


def get_account_service(database: Database = Depends(get_database)):
    return AccountService(database)
