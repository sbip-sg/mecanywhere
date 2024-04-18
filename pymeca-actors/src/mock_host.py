import asyncio
import hashlib
import pathlib
from ecies import decrypt
from web3 import Web3
import json
import websockets
import requests
import ipfs_api
from ecies.utils import generate_eth_key
import docker

import pymeca.utils
from pymeca.host import MecaHost
from cli import MecaCLI
import threading

config = json.load(open("../config/config.json", "r"))
TASK_EXECUTOR_URL = config["task_executor_url"]
IPFS_HOST = config["ipfs_gateway_host"]
IPFS_PORT = config["ipfs_gateway_port"]
BLOCKCHAIN_URL = config["blockchain_url"]
DAO_CONTRACT_ADDRESS = config["dao_contract_address"]
ACCOUNTS = json.load(open(config["accounts_path"], "r"))
CONTAINER_FOLDER = pathlib.Path(config["build_folder"])

CONTAINER_NAME_LIMIT = 10
DEFAULT_BLOCK_TIMEOUT_LIMIT = 10
RESOURCES = {
    "cpu": 16,
    "mem": 32000,
}


def download_from_ipfs(ipfs_cid):
    # Download IPFS folder in CONTAINER_FOLDER
    CONTAINER_FOLDER.mkdir(exist_ok=True)
    with ipfs_api.ipfshttpclient.connect(f"/dns/{IPFS_HOST}/tcp/{IPFS_PORT}/http") as client:
        client.get(ipfs_cid, target=CONTAINER_FOLDER)
    print("Downloaded IPFS folder.")


def build_docker_image(ipfs_cid):
    # Build docker image from IPFS folder
    with docker.APIClient() as client:
        generator = client.build(path=f"{CONTAINER_FOLDER}/{ipfs_cid}",
                                 tag=f"{ipfs_cid[-CONTAINER_NAME_LIMIT:]}",
                                 decode=True)
    while True:
        try:
            line = next(generator)
            print(line["stream"])
        except StopIteration:
            break
        except Exception as e:
            print(e)
    print("Built docker image.")


class TaskThread(threading.Thread):
    def __init__(self, kill_event, args=(), kwargs=None):
        self.kill_event = kill_event
        super().__init__(target=self.wrap_wait_for_task, args=args, kwargs=kwargs)

    def wrap_wait_for_task(self, mec_host, tower_uri, sk_hex):
        loop = asyncio.new_event_loop()
        loop.create_task(self.wait_for_task(mec_host, tower_uri, sk_hex))
        loop.run_forever()
        # asyncio.run(self.wait_for_task(mec_host, tower_uri, sk_hex))

    def stop(self):
        self.kill_event.set()
        asyncio.get_event_loop().stop()

    # wait for task from tower by setting up web socket
    async def wait_for_task(self, meca_host, tower_uri, sk_hex):    
        if tower_uri.startswith("http://"):
            tower_uri = tower_uri[len("http://"):]
        tower_uri = tower_uri.replace("localhost", "172.17.0.1", 1)
        host_address = meca_host.account.address
        async with websockets.connect(f'ws://{tower_uri}/ws/{host_address}') as websocket:
            print("Waiting for tasks on websocket...")
            while not self.kill_event.is_set():
                packet = await websocket.recv()
                json_packet = json.loads(packet)
                if "taskId" not in json_packet or "message" not in json_packet:
                    print("Invalid packet received.")
                    continue
                task_id = json_packet["taskId"]
                message_encrypted_str = json_packet["message"]
                message_decrypted_str = decrypt(sk_hex, bytes.fromhex(message_encrypted_str)).decode("utf-8")

                # Verify task on blockchain
                running_task = meca_host.get_running_task(task_id)
                if running_task is None:
                    print(f"Task {task_id} not found.")
                    continue
                # Verify message input
                calculated_hash = "0x" + hashlib.sha256(message_decrypted_str.encode("utf-8")).hexdigest()
                if running_task["inputHash"] != calculated_hash:
                    print("Task hash mismatch.")
                    continue

                print(f"Received task {task_id} from server")
                
                # format task executor request
                message = json.loads(message_decrypted_str)
                message["id"] = message["id"][-CONTAINER_NAME_LIMIT:] + ":latest"
                message["resource"] = RESOURCES

                # Send task to executor
                res = requests.post(TASK_EXECUTOR_URL, json=message)
                print(res.status_code)
                await websocket.send(res.text)


class MecaHostCLI(MecaCLI):
    def __init__(self):
        web3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))
        meca_host = MecaHost(
            w3=web3,
            private_key=ACCOUNTS["meca_host"]["private_key"],
            dao_contract_address=DAO_CONTRACT_ADDRESS,
        )
        print("Started host with address:", meca_host.account.address)
        super().__init__(meca_host)

        # Generate asymmetric keys for host decryption and user encryption
        eth_k = generate_eth_key()
        self.secret_key = eth_k.to_hex()
        self.public_key = eth_k.public_key.to_hex()

    async def run_func(self, func, args):
        if func.__name__ == "add_task":
            ipfs_sha = args[0]
            ipfs_cid = pymeca.utils.cid_from_sha256(ipfs_sha)
            download_from_ipfs(ipfs_cid)
            build_docker_image(ipfs_cid)
        print(func.__name__, ":")
        print(await super().run_func(func, args))

    
    def shutdown(self):
        for thread in threading.enumerate():
            if isinstance(thread, TaskThread):
                thread.stop()


async def main():
    cli = MecaHostCLI()
    meca_host = cli.actor
    sk = cli.secret_key
    default_public_key = cli.public_key

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
        tower_uri = meca_host.get_tower_public_uri(tower_address)
        kill_event = threading.Event()
        task_thread = TaskThread(kill_event, args=(meca_host, tower_uri, sk))
        task_thread.start()

    cli.add_method(wait_for_my_task)
    cli.add_method(meca_host.get_tasks)
    cli.add_method(meca_host.get_towers)
    await cli.start()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())