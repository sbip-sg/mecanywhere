import asyncio
import pathlib
import os
from web3 import Web3
import ipfs_api
from dotenv import load_dotenv
import pymeca

from cli import MecaCLI
from functions.user_functions import send_task_on_blockchain

load_dotenv()


BLOCKCHAIN_URL = os.getenv("MECA_BLOCKCHAIN_RPC_URL", None)
MECA_DAO_CONTRACT_ADDRESS = os.getenv("MECA_DAO_CONTRACT_ADDRESS", pymeca.dao.get_DAO_ADDRESS())
MECA_USER_PRIVATE_KEY = os.getenv("MECA_USER_PRIVATE_KEY", None)
OUTPUT_FOLDER = pathlib.Path("./build")

class MecaUserCLI(MecaCLI):
    def __init__(self):
        web3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))
        meca_user = pymeca.user.MecaUser(
            w3=web3,
            private_key=MECA_USER_PRIVATE_KEY,
            dao_contract_address=MECA_DAO_CONTRACT_ADDRESS,
        )
        print("Started user with address:", meca_user.account.address)
        super().__init__(meca_user)

    async def run_func(self, func, args):
        if func.__name__ == "send_task_on_blockchain":
            use_sgx = input(f"Enter use_sgx: ")
            use_sgx = use_sgx.lower() == "true"
            await send_task_on_blockchain(
                self.actor,
                args['ipfs_sha256'],
                args['host_address'],
                args['tower_address'],
                args['input_hash'],
                OUTPUT_FOLDER,
                use_sgx
            )
        elif func.__name__ == "get_tasks":
            print(func.__name__, ":")
            tasks = await super().run_func(func, args)
            with ipfs_api.ipfshttpclient.connect(f"/dns/{IPFS_HOST}/tcp/{IPFS_PORT}/http") as client:
                for i, task in enumerate(tasks):
                    ipfs_sha = task["ipfsSha256"]
                    ipfs_cid = pymeca.utils.cid_from_sha256(ipfs_sha)
                    description = client.cat(ipfs_cid + "/description.txt")
                    name = client.cat(ipfs_cid + "/name.txt")
                    print(f"Task {i+1})")
                    print(" Name:", name.decode("utf-8").strip())
                    print(" Description:", description.decode("utf-8").strip())
                    print(" Details:", task)
        else:
            print(func.__name__, ":")
            res = await super().run_func(func, args)
            print(res)
            return res


async def main():
    cli = MecaUserCLI()
    meca_user = cli.actor
    cli.add_method(meca_user.get_tasks)
    cli.add_method(meca_user.get_towers_hosts_for_task)
    await cli.start()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
