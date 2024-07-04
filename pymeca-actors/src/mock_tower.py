import asyncio
import os
from web3 import Web3
from dotenv import load_dotenv
import pymeca

from cli import MecaCLI

load_dotenv()

BLOCKCHAIN_URL = os.getenv("MECA_BLOCKCHAIN_RPC_URL", None)
MECA_DAO_CONTRACT_ADDRESS = os.getenv("MECA_DAO_CONTRACT_ADDRESS", pymeca.dao.get_DAO_ADDRESS())
MECA_TOWER_PRIVATE_KEY = os.getenv("MECA_TOWER_PRIVATE_KEY", None)


class MecaTowerCLI(MecaCLI):
    def __init__(self):
        web3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))
        meca_tower = pymeca.tower.MecaTower(
            w3=web3,
            private_key=MECA_TOWER_PRIVATE_KEY,
            dao_contract_address=MECA_DAO_CONTRACT_ADDRESS,
        )
        print("Started tower with address:", meca_tower.account.address)
        super().__init__(meca_tower)

    async def run_func(self, func, args):
        print(func.__name__, ":")
        print(await super().run_func(func, args))


async def main():
    cli = MecaTowerCLI()
    meca_tower = cli.actor

    # Register tower if not registered
    if not meca_tower.is_registered():
        print("\nTower is not registered. Registering...")
        default_size_limit = 10000
        default_public_connection = "http://172.17.0.1:7777"
        default_fee = 10
        default_fee_type = 0
        default_initial_deposit = meca_tower.get_tower_initial_stake()

        size_limit = int(input(f"Enter size limit: ({default_size_limit}) ").strip() or default_size_limit)
        public_connection = input(f"Enter public connection: ({default_public_connection}) ").strip() or default_public_connection
        fee = int(input(f"Enter fee: ({default_fee}) ").strip() or default_fee)
        fee_type = int(input(f"Enter fee type: ({default_fee_type}) ").strip() or default_fee_type)
        initial_deposit = int(input(f"Enter initial deposit: ({default_initial_deposit}) ").strip() or default_initial_deposit)
        meca_tower.register_tower(size_limit, public_connection, fee, fee_type, initial_deposit)
    print("Tower registered.")

    await cli.start()


if __name__ == '__main__':
    asyncio.run(main())
