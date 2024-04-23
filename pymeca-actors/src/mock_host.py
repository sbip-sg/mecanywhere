import asyncio
import websockets
import pathlib
import os
from ecies import encrypt
from ecies import decrypt
from web3 import Web3
from eth_hash.auto import keccak
import ipfs_api
import docker
from ecies.utils import generate_eth_key
import eth_keys
from dotenv import load_dotenv

import pymeca

from cli import MecaCLI

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
    "cpu": 16,
    "mem": 32000,
}


def download_from_ipfs(ipfs_cid):
    # Download IPFS folder in CONTAINER_FOLDER
    CONTAINER_FOLDER.mkdir(exist_ok=True)
    with ipfs_api.ipfshttpclient.connect(
        f"/dns/{MECA_IPFS_HOST}/tcp/{MECA_IPFS_PORT}/http"
    ) as client:
        client.get(ipfs_cid, target=CONTAINER_FOLDER)
    print("Downloaded IPFS folder.")


def build_docker_image(ipfs_cid):
    # Build docker image from IPFS folder
    with docker.APIClient() as client:
        generator = client.build(path=f"./{CONTAINER_FOLDER}/{ipfs_cid}",
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


async def connect_to_tower(meca_host, tower_address):
    tower_uri = meca_host.get_tower_public_uri(tower_address)
    tower_uri = tower_uri.replace("http://", "ws://")
    tower_uri = tower_uri.replace("https://", "wss://")
    tower_uri = f"{tower_uri}/host"
    async with websockets.connect(tower_uri) as websocket:
        print("Connected to tower.")
        token = await websocket.recv()
        print("Received token:", token.hex())
        # Send host address to tower
        host_address_bytes = pymeca.utils.bytes_from_hex(
            meca_host.account.address
        )
        to_send = host_address_bytes + token
        # sign the message
        signature = pymeca.utils.sign_bytes(
            private_key=MECA_HOST_ENCRYPTION_PRIVATE_KEY,
            message_bytes=to_send
        )
        to_send = to_send + signature
        await websocket.send(to_send)
        text_response = await websocket.recv()
        if text_response != "Host connected":
            print("Failed to connect to tower.")
            print(text_response)
            return

        print("Host connected to tower.")
        while True:
            input_bytes = await websocket.recv()
            print("Received input from tower.")
            task_id = "0x" + input_bytes[0:32].hex()
            print("Task ID:", task_id)
            signature = input_bytes[-65:]
            verify = pymeca.utils.verify_signature(
                signature_bytes=signature,
                message_bytes=input_bytes[0:-65]
            )
            if not verify:
                await websocket.send("Invalid signature")
                return

            user_eth_address = pymeca.utils.get_eth_address_hex_from_signature(
                signature_bytes=signature,
                message_bytes=input_bytes[0:-65]
            )
            user_eth_address = meca_host.w3.to_checksum_address(
                user_eth_address
            )
            user_public_key = pymeca.utils.get_public_key_from_signature(
                signature_bytes=signature,
                message_bytes=input_bytes[0:-65]
            )
            blockchain_task = meca_host.get_running_task(
                task_id=task_id
            )

            if blockchain_task is None:
                await websocket.send("Task not found")
                print("Task not found")
                return

            if blockchain_task["owner"] != user_eth_address:
                await websocket.send("Not the right owner")
                print("Not the right owner")
                return

            if blockchain_task["hostAddress"] != meca_host.account.address:
                await websocket.send("Wrong host")
                print("Wrong host")
                return
            if blockchain_task["towerAddress"] != tower_address:
                print("Wrong tower")
                await websocket.send("Wrong tower")
                return

            # decrypt the input
            input_message = decrypt(
                MECA_HOST_ENCRYPTION_PRIVATE_KEY,
                input_bytes[32:-65]
            )

            # verify the hash of the input
            input_hash = "0x" + keccak(input_message).hex()
            if blockchain_task["inputHash"] != input_hash:
                await websocket.send("Invalid input hash")
                print("Invalid input hash")
                return

            # run the task
            # TODO:
            # get task ipfs cid
            ipfs_sha256 = blockchain_task["ipfsSha256"]
            print("Task IPFS SHA256:", ipfs_sha256)
            # ipfs_cid = pymeca.utils.cid_from_sha256(ipfs_sha256)
            # verify is 0 sha so it is identity task
            if ipfs_sha256 == ("0x" + "0" * 64):
                output_bytes = input_message
            # else:
                # DO the task

            # hash the output
            print("Output:", output_bytes)
            output_hash = "0x" + keccak(output_bytes).hex()
            # send the output to the blockchain
            meca_host.register_task_output(
                task_id=task_id,
                output_hash=output_hash
            )

            # send the output to the user
            # encrypt the output
            output_encrypted = encrypt(
                user_public_key.to_hex(),
                output_bytes
            )
            to_send = input_bytes[0:32] + output_encrypted
            signature = pymeca.utils.sign_bytes(
                private_key=MECA_HOST_ENCRYPTION_PRIVATE_KEY,
                message_bytes=to_send
            )
            to_send = to_send + signature
            await websocket.send(to_send)
            print("Sent output to user.")
            text_reply = await websocket.recv()
            if text_reply != "Task output sent":
                print("Problems with the websocket")
                print(text_reply)
            else:
                print("Task output sent")


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

        # Generate asymmetric keys for host decryption and user encryption
        eth_k = generate_eth_key()
        self.secret_key = eth_k.to_hex()
        self.public_key = eth_k.public_key.to_hex()

    async def run_func(self, func, args):
        if func.__name__ == "add_task":
            ipfs_sha = args[0]
            if ipfs_sha != ("0x" + "0" * 64):
                ipfs_cid = pymeca.utils.cid_from_sha256(ipfs_sha)
                download_from_ipfs(ipfs_cid)
                build_docker_image(ipfs_cid)
        print(func.__name__, ":")
        print(await super().run_func(func, args))


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
        await connect_to_tower(meca_host, tower_address)

    cli.add_method(wait_for_my_task)
    cli.add_method(meca_host.get_tasks)
    cli.add_method(meca_host.get_towers)
    await cli.start()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
