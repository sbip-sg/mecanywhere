import asyncio
import base64
import json
import websockets
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5, AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from ecies import encrypt
from ecies import decrypt
from eth_hash.auto import keccak

import pymeca


async def wait_for_task(actor: pymeca.user.MecaUser, websocket, task_id, output_folder, use_sgx=False, output_key = None):
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
    print("message: ", message)
    if not use_sgx:
        output_hash = runningTask["outputHash"]
        received_hash = "0x" + keccak(message).hex()
        if output_hash != received_hash:
            print("Output hash mismatch")
            return
        print("Task output hash verified.")
    elif output_key is not None:
        # decrypt the message
        print("Decrypting the enclave output")
        encrypted_output = json.loads(message)["msg"]
        print("enclave encrypted output: ", encrypted_output)
        encrypted_output = bytes.fromhex(json.loads(encrypted_output)["msg"])
        print("enclave encrypted output bytes:", encrypted_output)
        tag = encrypted_output[-16:]
        iv = encrypted_output[-12-16:-16]
        encrypted_data = encrypted_output[:-12-16]
        # decrypt the output
        aes_gcm_128_cipher = AES.new(key=output_key, mode=AES.MODE_GCM, nonce=iv)
        message = aes_gcm_128_cipher.decrypt_and_verify(encrypted_data, tag)


    if runningTask["ipfsSha256"] == ("0x" + "0" * 64):
        print("Output: ", message)
    else:
        with open(f"{output_folder}/output.txt", "wb") as f:
            f.write(message)
        # output_folder.mkdir(exist_ok=True)
        # with open(f"{output_folder}/output.png", "wb") as f:
        #     f.write(base64.b64decode(message))

    print("Task output saved to output.txt")
    # also return the result
    print(message)
    return message

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
        output_folder,
        use_sgx : bool
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
        output_key = None
        if use_sgx:
            async with websockets.connect(tower_uri) as websocket:
                # prepare ra_input
                ra_input = {
                    "id": ipfs_cid,
                    "input": "SGXRAREQUEST",
                    "use_sgx": True
                }
                ra_input_bytes = json.dumps(ra_input).encode()
                encrypted_ra_input_bytes = encrypt(
                    blockcahin_host_pub_key,
                    ra_input_bytes
                )
                ra_to_send = task_id_bytes + encrypted_ra_input_bytes
                ra_input_signature = actor.sign_bytes(ra_to_send)
                ra_to_send = ra_to_send + ra_input_signature

                await websocket.send(ra_to_send)
                response_text = await websocket.recv()
                print(response_text)
                if response_text != "Task connected":
                    print("Task connection failed")
                    return
                host_resp = await wait_for_task(actor, websocket, task_id, output_folder, use_sgx=True)
                print("Host response: ", host_resp)
                host_resp = json.loads(host_resp)
                print("Host json: ", host_resp)
                if not host_resp["success"]:
                    print("RA failed")
                    return
                enclave_msg =json.loads(host_resp["msg"])
                print("enclave msg: ", enclave_msg)
                # raise NotImplementedError("SGX workflow after ra not implemented")

                # setup the session key and output key
                session_key = get_random_bytes(32)
                output_key = get_random_bytes(16)

                pub_key_data = enclave_msg["msg"]["key"]

                try:
                    public_key = RSA.importKey(pub_key_data)
                except Exception as e:
                    print(e)
                    return
                
                rsa_cipher = PKCS1_v1_5.new(public_key)
                # not specifying iv here, python aes will generate a random one
                print("session key len: ", len(session_key))
                aes_cipher = AES.new(key=session_key, mode=AES.MODE_CBC)
                # retrieve the iv
                iv = aes_cipher.iv
                sensitive_data = bytes(input, "utf-8")+output_key
                padded_sensitive_data = pad(sensitive_data, AES.block_size)
                encrypted_data = aes_cipher.encrypt(padded_sensitive_data)
                encrypted_key = rsa_cipher.encrypt(session_key)
                # assemble the message
                encrypted_message = encrypted_data + encrypted_key + iv

                print("encrypted key size: ", len(encrypted_key))
                print("encrypted message length: ", len(encrypted_message))

                data = {
                    "value": encrypted_message.hex()
                }
                input_with_id = {
                    "id": ipfs_cid,
                    # hex encode the encrypted message
                    "input": json.dumps(data),
                    "use_sgx": True
                }
                input_bytes = json.dumps(input_with_id).encode()
                input_hash = "0x" + keccak(input_bytes).hex()
                encrypted_input_bytes = encrypt(
                    blockcahin_host_pub_key,
                    input_bytes
                )
                to_send = task_id_bytes + encrypted_input_bytes
                signature = actor.sign_bytes(to_send)
                to_send = to_send + signature
                print (to_send)


        async with websockets.connect(tower_uri) as websocket:
            await websocket.send(to_send)
            response_text = await websocket.recv()
            print(response_text)
            if response_text != "Task connected":
                print("Task connection failed")
                return
            tasks = [
                asyncio.ensure_future(
                    wait_for_task(actor, websocket, task_id, output_folder, use_sgx=use_sgx, output_key=output_key)
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
