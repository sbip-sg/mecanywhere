from functools import lru_cache
from fastapi import Depends
from web3 import Web3
from pymeca.tower import MecaTower
from pymeca.dao import get_DAO_ADDRESS

from config import Config

def get_dao_address():
    return get_DAO_ADDRESS()

@lru_cache()
def get_config():
    return Config(
        "../config.json",
    )

def get_web3(config: Config = Depends(get_config)):
    return Web3(Web3.HTTPProvider(config.get_blockchain_provider_url()))

def get_meca_tower(config: Config = Depends(get_config), web3: Web3 = Depends(get_web3)) -> MecaTower:
    meca_tower = MecaTower(
        w3=web3,
        private_key=config.get_tower_private_key(),
        dao_contract_address=get_dao_address(),
    )
    return meca_tower
