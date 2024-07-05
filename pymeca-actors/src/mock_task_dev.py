import asyncio
from web3 import Web3
import os
from dotenv import load_dotenv
import pymeca
from cli import MecaCLI
from functions.task_dev_functions import add_folder_to_ipfs_host

load_dotenv()

MECA_IPFS_API_HOST = os.getenv("MECA_IPFS_API_HOST", None)
MECA_IPFS_API_PORT = os.getenv("MECA_IPFS_API_PORT", None)
BLOCKCHAIN_URL = os.getenv("MECA_BLOCKCHAIN_RPC_URL", None)
MECA_DAO_CONTRACT_ADDRESS = os.getenv("MECA_DAO_CONTRACT_ADDRESS", pymeca.dao.get_DAO_ADDRESS())
MECA_DEV_PRIVATE_KEY = os.getenv("MECA_DEV_PRIVATE_KEY", None)


class TaskDeveloperCLI(MecaCLI):
    def __init__(self):
        web3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))
        meca_task_developer = pymeca.task.MecaTaskDeveloper(
            w3=web3,
            private_key=MECA_DEV_PRIVATE_KEY,
            dao_contract_address=MECA_DAO_CONTRACT_ADDRESS,
        )
        print(
            "Started task dev with address:",
            meca_task_developer.account.address
        )
        super().__init__(meca_task_developer)

    async def run_func(self, func, args):
        print(func.__name__, ":")
        res = await super().run_func(func, args)
        print(res)
        return res


async def main():
    cli = TaskDeveloperCLI()
    cli.add_method(pymeca.utils.get_sha256_from_cid)

    async def add_folder_to_ipfs(folder_path: str):
        await add_folder_to_ipfs_host(folder_path, MECA_IPFS_API_HOST, MECA_IPFS_API_PORT)

    cli.add_method(add_folder_to_ipfs)
    await cli.start()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
