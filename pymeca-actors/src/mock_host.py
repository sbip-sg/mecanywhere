import asyncio
import threading
import pathlib
import os
from web3 import Web3
import eth_keys
from dotenv import load_dotenv

import pymeca

from cli import MecaCLI
from functions.host_functions import download_from_ipfs, build_docker_image, TaskThread

load_dotenv()


BLOCKCHAIN_URL = os.getenv("MECA_BLOCKCHAIN_RPC_URL", None)
MECA_DAO_CONTRACT_ADDRESS = pymeca.dao.get_DAO_ADDRESS()
MECA_HOST_PRIVATE_KEY = os.getenv("MECA_HOST_PRIVATE_KEY", None)
MECA_HOST_ENCRYPTION_PRIVATE_KEY = os.getenv(
    "MECA_HOST_ENCRYPTION_PRIVATE_KEY",
    None
)
OUTPUT_FOLDER = pathlib.Path("./build")
MECA_TASK_EXECUTOR_URL = os.getenv(
    "MECA_TASK_EXECUTOR_URL",
    None
)
MECA_IPFS_HOST = os.getenv("MECA_IPFS_HOST", None)
MECA_IPFS_PORT = os.getenv("MECA_IPFS_PORT", None)
CONTAINER_FOLDER = pathlib.Path("./build")

CONTAINER_NAME_LIMIT = 10
DEFAULT_BLOCK_TIMEOUT_LIMIT = 10
RESOURCES = {
    # "cpu": 16,
    # "mem": 32000,
    "cpu": 1,
    "mem": 128,
}


class MecaHostCLI(MecaCLI):
    def __init__(self):
        web3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))
        meca_host = pymeca.host.MecaHost(
            w3=web3,
            private_key=MECA_HOST_PRIVATE_KEY,
            dao_contract_address=MECA_DAO_CONTRACT_ADDRESS,
        )
        print("Started host with address:", meca_host.account.address)
        super().__init__(meca_host)

    async def run_func(self, func, args):
        if func.__name__ == "add_task":
            ipfs_sha = args['ipfs_sha256']
            if ipfs_sha != ("0x" + "0" * 64):
                ipfs_cid = pymeca.utils.cid_from_sha256(ipfs_sha)
                download_from_ipfs(ipfs_cid, CONTAINER_FOLDER, MECA_IPFS_HOST, MECA_IPFS_PORT)
                build_docker_image(ipfs_cid, CONTAINER_FOLDER, CONTAINER_NAME_LIMIT)
        print(func.__name__, ":")
        res = await super().run_func(func, args)
        print(res)
        return res

    def shutdown(self):
        for thread in threading.enumerate():
            if isinstance(thread, TaskThread):
                thread.stop()

async def main():
    cli = MecaHostCLI()
    meca_host = cli.actor
    enc_priv_key = eth_keys.keys.PrivateKey(
        pymeca.utils.bytes_from_hex(MECA_HOST_ENCRYPTION_PRIVATE_KEY)
    )
    default_public_key = enc_priv_key.public_key.to_hex()

    # Register host if not registered
    if not meca_host.is_registered():
        default_block_timeout_limit = DEFAULT_BLOCK_TIMEOUT_LIMIT
        default_initial_deposit = meca_host.get_host_initial_stake()

        print("\nHost is not registered. Registering...")
        block_timeout_limit = int(input(f"Enter block timeout limit: ({default_block_timeout_limit}) ").strip() or default_block_timeout_limit)
        public_key = input(f"Enter public key: ({default_public_key}) ").strip() or default_public_key
        initial_deposit = int(input(f"Enter initial deposit: ({default_initial_deposit}) ").strip() or default_initial_deposit)
        meca_host.register(block_timeout_limit, public_key, initial_deposit)
    else:
        meca_host.update_block_timeout_limit(DEFAULT_BLOCK_TIMEOUT_LIMIT)
        print("Host block timeout limit updated.")
        meca_host.update_public_key(default_public_key)
        print("Host public key updated.")
    print("Host registered.")

    # Blocking function to wait for tasks from a given tower
    async def wait_for_my_task(tower_address: str):
        kill_event = threading.Event()
        task_thread = TaskThread(kill_event, args=(
            meca_host,
            tower_address,
            MECA_HOST_ENCRYPTION_PRIVATE_KEY,
            CONTAINER_NAME_LIMIT,
            RESOURCES,
            MECA_TASK_EXECUTOR_URL
        ))
        task_thread.start()

    cli.add_method(wait_for_my_task)
    cli.add_method(meca_host.get_tasks)
    cli.add_method(meca_host.get_towers)
    await cli.start()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
