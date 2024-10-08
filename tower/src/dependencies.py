from functools import lru_cache
import os
from web3 import Web3
from pymeca.tower import MecaTower
from config import Config


@lru_cache()
def get_config():
    return Config(
        os.path.join(os.path.dirname(__file__), "../config.json"),
    )

def get_web3(config: Config = get_config()):
    return Web3(Web3.HTTPProvider(config.get_blockchain_provider_url()))

def get_meca_tower(config: Config = get_config(), web3: Web3 = get_web3()) -> MecaTower:
    meca_tower = MecaTower(
        w3=web3,
        private_key=config.get_tower_private_key(),
        dao_contract_address=config.get_dao_contract_address(),
    )
    return meca_tower
