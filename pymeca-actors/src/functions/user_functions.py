import asyncio
import base64
import json
import websockets
from ecies import encrypt
from ecies import decrypt
from eth_hash.auto import keccak

import pymeca


async def wait_for_task(actor: pymeca.user.MecaUser, websocket, task_id, output_folder):
    task_output = await websocket.recv()
    print("Task output received.")
    print(task_output)
    task_id = "0x" + task_output[0:32].hex()
    signature = task_output[-65:]
    verify = pymeca.utils.verify_signature(
        signature_bytes=signature,
        message_bytes=task_output[0:-65]
    )
    if not verify:
        print("Signature verification failed.")
        return
    host_ecc_pub_key = pymeca.utils.get_public_key_from_signature(
        signature_bytes=signature,
        message_bytes=task_output[0:-65]
    )
    host_ecc_pub_key_hex = host_ecc_pub_key.to_hex()

    runningTask = actor.get_running_task(task_id)
    host_address = runningTask["hostAddress"]
    blockcahin_host_pub_key = actor.get_host_public_key(
        host_address
    )

    if host_ecc_pub_key_hex != blockcahin_host_pub_key:
        print("Invalid host encryption public key")
        return

    encrypted_message = task_output[32:-65]
    message = decrypt(
        actor.private_key,
        encrypted_message
    )

    output_hash = runningTask["outputHash"]
    received_hash = "0x" + keccak(message).hex()
    if output_hash != received_hash:
        print("Output hash mismatch")
        return

    print("Task output hash verified.")

    if runningTask["ipfsSha256"] == ("0x" + "0" * 64):
        print("Output: ", message)
    else:
        with open(f"{output_folder}/output.txt", "wb") as f:
            f.write(message)
        # output_folder.mkdir(exist_ok=True)
        # with open(f"{output_folder}/output.png", "wb") as f:
        #     f.write(base64.b64decode(message))

    print("Task output saved to output.png")

async def finish_task(actor: pymeca.user.MecaUser, task_id):
    # wait for the task to be over on blockchain
    while not actor.is_task_done(task_id=task_id):
        await asyncio.sleep(1)

    actor.finish_task(task_id=task_id)
    print("sent finish task transaction.")

async def send_task_on_blockchain(
        actor: pymeca.user.MecaUser,
        ipfs_sha, 
        host_address, 
        tower_address, 
        input, 
        output_folder
    ):
        ipfs_cid = pymeca.utils.cid_from_sha256(ipfs_sha)
        input_with_id = {
            "id": ipfs_cid,
            "input": input,
        }
        input_bytes = json.dumps(input_with_id).encode()
        # because I set the input in pymeca as a hex string
        input_hash = "0x" + keccak(input_bytes).hex()
        success, task_id = actor.send_task_on_blockchain(
            ipfs_sha256=ipfs_sha,
            host_address=host_address,
            tower_address=tower_address,
            input_hash=input_hash
        )
        print("Task id: ", task_id)
        tower_url = actor.get_tower_public_uri(tower_address)
        blockcahin_host_pub_key = actor.get_host_public_key(
            host_address
        )
        encrypted_input_bytes = encrypt(
            blockcahin_host_pub_key,
            input_bytes
        )
        task_id_bytes = pymeca.utils.bytes_from_hex(task_id)
        to_send = task_id_bytes + encrypted_input_bytes
        signature = actor.sign_bytes(to_send)
        to_send = to_send + signature
        tower_uri = tower_url.replace("http://", "ws://")
        tower_uri = tower_uri.replace("https://", "wss://")
        tower_uri = f"{tower_uri}/client"
        async with websockets.connect(tower_uri) as websocket:
            await websocket.send(to_send)
            reponse_text = await websocket.recv()
            print(reponse_text)
            if reponse_text != "Task connected":
                print("Task connection failed")
                return
            tasks = [
                asyncio.ensure_future(
                    wait_for_task(actor, websocket, task_id, output_folder)
                ),
                asyncio.ensure_future(
                    finish_task(actor, task_id)
                )
            ]
            finished, unfinished = await asyncio.wait(
                tasks,
                return_when=asyncio.FIRST_COMPLETED
            )
            if tasks[0] in unfinished:
                tasks[0].cancel()
            else:
                await tasks[1]
