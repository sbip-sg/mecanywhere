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
        generator = client.build(path=f"./{container_folder}/{ipfs_cid}",
                                 tag=f"{ipfs_cid[-container_name_limit:]}",
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

    def wrap_wait_for_task(
            self,
            mec_host,
            tower_address,
            host_encryption_private_key,
            container_name_limit,
            resources,
            task_executor_url
        ):
        loop = asyncio.new_event_loop()
        loop.create_task(self.connect_to_tower(
            mec_host, 
            tower_address,
            host_encryption_private_key,
            container_name_limit,
            resources,
            task_executor_url
        ))
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
            resources, 
            task_executor_url
        ):
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
                private_key=host_encryption_private_key,
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
                    host_encryption_private_key,
                    input_bytes[32:-65]
                )

                # verify the hash of the input
                input_hash = "0x" + keccak(input_message).hex()
                if blockchain_task["inputHash"] != input_hash:
                    await websocket.send("Invalid input hash")
                    print("Invalid input hash")
                    return

                # run the task
                ipfs_sha256 = blockchain_task["ipfsSha256"]
                print("Task IPFS SHA256:", ipfs_sha256)
                # verify is 0 sha so it is identity task
                if ipfs_sha256 == ("0x" + "0" * 64):
                    output_bytes = input_message
                else:
                    # DO the task
                    message_dict = json.loads(input_message)
                    message_dict["id"] = message_dict["id"][-container_name_limit:] + ":latest"
                    message_dict["resource"] = resources

                    # Send task to executor
                    res = requests.post(task_executor_url, json=message_dict)
                    print(res.status_code)
                    output_bytes = res.content

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
                    private_key=host_encryption_private_key,
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
