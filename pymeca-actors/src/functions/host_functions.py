import asyncio
import json
import threading
import requests
import websockets
from ecies import encrypt
from ecies import decrypt
from eth_hash.auto import keccak
import ipfs_api
import docker
import pymeca


def download_from_ipfs(ipfs_cid, container_folder, ipfs_host, ipfs_port):
    # Download IPFS folder in CONTAINER_FOLDER
    container_folder.mkdir(exist_ok=True)
    with ipfs_api.ipfshttpclient.connect(
        f"/dns/{ipfs_host}/tcp/{ipfs_port}/http"
    ) as client:
        client.get(ipfs_cid, target=container_folder)
    print("Downloaded IPFS folder.")


def build_docker_image(ipfs_cid, container_folder, container_name_limit):
    # Build docker image from IPFS folder
    with docker.APIClient() as client:
        generator = client.build(
            path=f"./{container_folder}/{ipfs_cid}",
            tag=f"{ipfs_cid[-container_name_limit:]}",
            decode=True,
        )
    while True:
        try:
            line = next(generator)
            print(line["stream"])
        except StopIteration:
            break
        except Exception as e:
            print(e)
    print("Built docker image.")


def get_resources_from_task(ipfs_host, ipfs_port, ipfs_cid):
    with ipfs_api.ipfshttpclient.connect(
        f"/dns/{ipfs_host}/tcp/{ipfs_port}/http"
    ) as client:
        f = client.cat(f"{ipfs_cid}/config.json")
        resources = json.loads(f.decode('utf-8'))
    if resources is None:
        resources = {}
    return resources


def sign_message(private_key, message):
    # Sign the message
    signature = pymeca.utils.sign_bytes(private_key=private_key, message_bytes=message)
    return message + signature


def encrypt_and_sign_output(
    private_key: str, enc_key: str, task_id_bytes: bytes, output_bytes: bytes
):
    # Encrypt the output
    output_encrypted = encrypt(enc_key, output_bytes)
    to_send = task_id_bytes + output_encrypted
    return sign_message(private_key, to_send)


def format_tower_uri_for_host(tower_uri):
    # Format the tower URI for the host
    tower_uri = tower_uri.replace("http://", "ws://")
    tower_uri = tower_uri.replace("https://", "wss://")
    return tower_uri + "/host"


def verify_and_parse_task_input(
    actor,
    task_input: bytes,
    host_encryption_private_key: str,
    tower_address: str,
):
    # Verify signature
    task_id = "0x" + task_input[0:32].hex()
    signature = task_input[-65:]
    verify = pymeca.utils.verify_signature(
        signature_bytes=signature, message_bytes=task_input[0:-65]
    )
    if not verify:
        raise ValueError("Invalid signature")

    # get the signer
    user_eth_address = pymeca.utils.get_eth_address_hex_from_signature(
        signature_bytes=signature, message_bytes=task_input[0:-65]
    )
    user_eth_address = actor.w3.to_checksum_address(user_eth_address)
    user_public_key = pymeca.utils.get_public_key_from_signature(
        signature_bytes=signature, message_bytes=task_input[0:-65]
    )

    # verify task on-chain meta
    blockchain_task = actor.get_running_task(task_id=task_id)
    if blockchain_task is None:
        raise ValueError("Task not found")
    if blockchain_task["owner"] != user_eth_address:
        raise ValueError("Not the right owner")
    if blockchain_task["hostAddress"] != actor.account.address:
        raise ValueError("Wrong host")
    if blockchain_task["towerAddress"] != tower_address:
        raise ValueError("Wrong tower")

    # decrypt the input
    task_input = decrypt(host_encryption_private_key, task_input[32:-65])

    # parse the input
    message_dict = json.loads(task_input)
    print("Input:", message_dict)

    # verify the input hash
    input_hash = "0x" + keccak(task_input).hex()
    if "use_sgx" not in message_dict or not message_dict["use_sgx"]:
        if blockchain_task["inputHash"] != input_hash:
            raise ValueError("Invalid input hash")
    else:
        if message_dict["input"] == "SGXRAREQUEST":
            if blockchain_task["inputHash"] != input_hash:
                raise ValueError("Invalid input hash")
        else:
            tee_task = actor.get_tee_task(task_id)
            if tee_task is None:
                raise ValueError("TEE task not found")
            if not tee_task["encryptedInputHash"]:
                raise ValueError("Encrypted input hash not found")
            if tee_task["encryptedInputHash"] != input_hash:
                raise ValueError("Invalid encrypted input hash")

    return message_dict, task_id, user_public_key, blockchain_task["ipfsSha256"]

class TaskThread(threading.Thread):
    def __init__(self, kill_event, args=(), kwargs=None):
        self.kill_event = kill_event
        super().__init__(target=self.wrap_wait_for_task, args=args, kwargs=kwargs)

    def wrap_wait_for_task(
        self,
        mec_host,
        tower_address,
        host_encryption_private_key,
        container_name_limit,
        task_executor_url,
        ipfs_host,
        ipfs_port,
    ):
        loop = asyncio.new_event_loop()
        loop.create_task(
            self.connect_to_tower(
                mec_host,
                tower_address,
                host_encryption_private_key,
                container_name_limit,
                task_executor_url,
                ipfs_host,
                ipfs_port,
            )
        )
        loop.run_forever()
        # asyncio.run(self.wait_for_task(mec_host, tower_address))

    def stop(self):
        self.kill_event.set()
        asyncio.get_event_loop().stop()

    async def connect_to_tower(
        self,
        meca_host,
        tower_address,
        host_encryption_private_key,
        container_name_limit,
        task_executor_url,
        ipfs_host,
        ipfs_port,
    ):
        tower_uri = format_tower_uri_for_host(
            meca_host.get_tower_public_uri(tower_address)
        )
        async with websockets.connect(tower_uri) as websocket:
            print("Connected to tower.")
            token = await websocket.recv()
            print("Received token:", token.hex())
            # Send host address to tower
            host_address_bytes = pymeca.utils.bytes_from_hex(meca_host.account.address)
            to_send = host_address_bytes + token
            await websocket.send(sign_message(host_encryption_private_key, to_send))
            text_response = await websocket.recv()
            if text_response != "Host connected":
                print("Failed to connect to tower.")
                print(text_response)
                raise ValueError("Failed to connect to tower.", text_response)

            print("Host connected to tower.")
            while True:
                input_bytes = await websocket.recv()
                print("Received input from tower.")
                # parse and verify the input
                try:
                    message_dict, task_id, user_public_key, task_ipfs_sha256 = (
                        verify_and_parse_task_input(
                            meca_host,
                            input_bytes,
                            host_encryption_private_key,
                            tower_address,
                        )
                    )
                except ValueError as e:
                    print(e)
                    await websocket.send(sign_message(host_encryption_private_key, repr(e).encode()))

                try:
                    # run the task
                    if task_ipfs_sha256 == ("0x" + "0" * 64):
                        output_bytes = json.dumps(message_dict).encode()
                    else:
                        # DO the task
                        message_dict["id"] = (
                            message_dict["id"][-container_name_limit:] + ":latest"
                        )
                        message_dict["resource"] = get_resources_from_task(
                            ipfs_host,
                            ipfs_port,
                            pymeca.utils.cid_from_sha256(task_ipfs_sha256)
                        )

                        # Send task to executor
                        print("Sending:", message_dict)
                        res = requests.post(task_executor_url, json=message_dict)
                        print(res.status_code)
                        output_bytes = res.content

                    # hash the output
                    print("Output:", output_bytes)
                    output_hash = "0x" + keccak(output_bytes).hex()

                    if message_dict["input"] != "SGXRAREQUEST":
                        # send the output to the blockchain
                        meca_host.register_task_output(
                            task_id=task_id, output_hash=output_hash
                        )

                    # send the output to the user
                    await websocket.send(
                        encrypt_and_sign_output(
                            host_encryption_private_key,
                            user_public_key.to_hex(),
                            input_bytes[0:32],
                            output_bytes,
                        )
                    )
                    print("Sent output to user.")
                    text_reply = await websocket.recv()
                    if text_reply != "Task output sent":
                        print("Problems with the websocket")
                        print(text_reply)
                    else:
                        print("Task output sent")
                except Exception as e:
                    print(e)
                    await websocket.send(sign_message(host_encryption_private_key, repr(e).encode()))
