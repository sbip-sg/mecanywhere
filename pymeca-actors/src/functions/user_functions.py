import asyncio
import json
import websockets
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5, AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from ecies import encrypt
from ecies import decrypt
from eth_hash.auto import keccak
import ipfs_api

import pymeca


def prepare_input(ipfs_cid: str, input: any, use_sgx: bool):
    input_with_id = (
        {"id": ipfs_cid, "input": input, "use_sgx": True}
        if use_sgx
        else {"id": ipfs_cid, "input": input}
    )
    input_bytes = json.dumps(input_with_id).encode()
    return input_bytes


def encrypt_and_sign_input(
    actor: pymeca.user.MecaUser, enc_key: str, input_bytes: bytes, task_id: bytes
):
    encrypted_input_bytes = encrypt(enc_key, input_bytes)
    to_send = task_id + encrypted_input_bytes
    signature = actor.sign_bytes(to_send)
    to_send = to_send + signature
    return to_send


def encrypt_sgx_task_input(enclave_msg: dict, output_key: bytes, input_bytes: bytes):
    pub_key_data = enclave_msg["msg"]["key"]
    public_key = RSA.importKey(pub_key_data)
    rsa_cipher = PKCS1_v1_5.new(public_key)
    # not specifying iv here, python aes will generate a random one

    session_key = get_random_bytes(32)
    print("session key len: ", len(session_key))
    aes_cipher = AES.new(key=session_key, mode=AES.MODE_CBC)
    # retrieve the iv
    iv = aes_cipher.iv
    sensitive_data = bytes(input_bytes, "utf-8") + output_key
    padded_sensitive_data = pad(sensitive_data, AES.block_size)
    encrypted_data = aes_cipher.encrypt(padded_sensitive_data)
    encrypted_key = rsa_cipher.encrypt(session_key)
    # assemble the message
    encrypted_message = encrypted_data + encrypted_key + iv

    print("encrypted key size: ", len(encrypted_key))
    print("encrypted message length: ", len(encrypted_message))
    return encrypted_message


def decrypt_sgx_task_output(output_bytes: bytes, output_key: bytes) -> bytes:
    # decrypt the message
    print("Decrypting the enclave output")
    encrypted_output = json.loads(output_bytes)["msg"]
    print("enclave encrypted output: ", encrypted_output)
    encrypted_output = bytes.fromhex(json.loads(encrypted_output)["msg"])
    tag = encrypted_output[-16:]
    iv = encrypted_output[-12 - 16 : -16]
    encrypted_data = encrypted_output[: -12 - 16]
    # decrypt the output
    aes_gcm_128_cipher = AES.new(key=output_key, mode=AES.MODE_GCM, nonce=iv)
    return aes_gcm_128_cipher.decrypt_and_verify(encrypted_data, tag)


def format_tower_uri_for_client(tower_uri: str):
    tower_uri = tower_uri.replace("http://", "ws://")
    tower_uri = tower_uri.replace("https://", "wss://")
    tower_uri = f"{tower_uri}/client"
    return tower_uri


def verify_and_parse_task_output(
    actor: pymeca.user.MecaUser, task_output: bytes, verify_output_hash: bool = True
):
    task_id = "0x" + task_output[0:32].hex()

    # verify signature
    signature = task_output[-65:]
    verify = pymeca.utils.verify_signature(
        signature_bytes=signature, message_bytes=task_output[0:-65]
    )
    if not verify:
        raise ValueError("Signature verification failed.")

    runningTask = actor.get_running_task(task_id)
    # verify signed by the right host
    host_ecc_pub_key = pymeca.utils.get_public_key_from_signature(
        signature_bytes=signature, message_bytes=task_output[0:-65]
    )
    host_ecc_pub_key_hex = host_ecc_pub_key.to_hex()
    host_address = runningTask["hostAddress"]
    blockcahin_host_pub_key = actor.get_host_public_key(host_address)
    if host_ecc_pub_key_hex != blockcahin_host_pub_key:
        raise ValueError("Invalid host encryption public key")

    # decrypt the message with host key
    encrypted_message = task_output[32:-65]
    message = decrypt(actor.private_key, encrypted_message)
    print("message: ", message)

    # verify the output message hash
    if verify_output_hash:
        output_hash = runningTask["outputHash"]
        received_hash = "0x" + keccak(message).hex()
        if output_hash != received_hash:
            raise ValueError("Output hash mismatch")
        print("Task output hash verified.")

    return message


async def wait_for_task(
    actor: pymeca.user.MecaUser,
    websocket,
    task_id,
    output_folder,
    use_sgx=False,
    output_key=None,
):
    task_output = await websocket.recv()
    print("Task output received.")
    message = verify_and_parse_task_output(
        actor, task_output, verify_output_hash=not use_sgx
    )

    if use_sgx and output_key is not None:
        message = decrypt_sgx_task_output(message, output_key)

    output_folder.mkdir(exist_ok=True)
    with open(f"{output_folder}/output.txt", "wb") as f:
        f.write(message)
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
    use_sgx: bool = False,
):
    ipfs_cid = pymeca.utils.cid_from_sha256(ipfs_sha)
    input_bytes = prepare_input(ipfs_cid, input, use_sgx)
    # because I set the input in pymeca as a hex string
    input_hash = "0x" + keccak(input_bytes).hex()
    success, task_id = actor.send_task_on_blockchain(
        ipfs_sha256=ipfs_sha,
        host_address=host_address,
        tower_address=tower_address,
        input_hash=input_hash,
    )
    print("Task id: ", task_id)
    blockcahin_host_pub_key = actor.get_host_public_key(host_address)
    task_id_bytes = pymeca.utils.bytes_from_hex(task_id)
    to_send = encrypt_and_sign_input(
        actor, blockcahin_host_pub_key, input_bytes, task_id_bytes
    )
    tower_uri = format_tower_uri_for_client(actor.get_tower_public_uri(tower_address))
    output_key = None
    if use_sgx:
        async with websockets.connect(tower_uri) as websocket:
            ra_input_bytes = prepare_input(ipfs_cid, "SGXRAREQUEST", use_sgx=True)
            ra_to_send = encrypt_and_sign_input(
                actor, blockcahin_host_pub_key, ra_input_bytes, task_id_bytes
            )

            await websocket.send(ra_to_send)
            response_text = await websocket.recv()
            # print(response_text)
            if response_text != "Task connected":
                print("Task connection failed")
                return
            host_resp = await wait_for_task(
                actor, websocket, task_id, output_folder, use_sgx=True
            )
            # print("Host response: ", host_resp)
            host_resp = json.loads(host_resp)
            # print("Host json: ", host_resp)
            if not host_resp["success"]:
                print("RA failed")
                return
            enclave_msg = json.loads(host_resp["msg"])
            # print("enclave msg: ", enclave_msg)

            # setup the session key and output key
            output_key = get_random_bytes(16)
            try:
                encrypted_message = encrypt_sgx_task_input(
                    enclave_msg, output_key, input
                )
            except Exception as e:
                print(e)
                return

            # prepare task input
            input_bytes = prepare_input(
                ipfs_cid, json.dumps({"value": encrypted_message.hex()}), use_sgx=True
            )
            to_send = encrypt_and_sign_input(
                actor, blockcahin_host_pub_key, input_bytes, task_id_bytes
            )

    async with websockets.connect(tower_uri) as websocket:
        await websocket.send(to_send)
        response_text = await websocket.recv()
        print(response_text)
        if response_text != "Task connected":
            print("Task connection failed")
            return
        tasks = [
            asyncio.ensure_future(
                wait_for_task(
                    actor,
                    websocket,
                    task_id,
                    output_folder,
                    use_sgx=use_sgx,
                    output_key=output_key,
                )
            ),
            asyncio.ensure_future(finish_task(actor, task_id)),
        ]
        finished, unfinished = await asyncio.wait(
            tasks, return_when=asyncio.FIRST_COMPLETED
        )
        if tasks[0] in unfinished:
            tasks[0].cancel()
        else:
            await tasks[1]

def print_task_details_from_ipfs(tasks, ipfs_host, ipfs_port):
    with ipfs_api.ipfshttpclient.connect(f"/dns/{ipfs_host}/tcp/{ipfs_port}/http") as client:
        for i, task in enumerate(tasks):
            ipfs_sha = task["ipfsSha256"]
            ipfs_cid = pymeca.utils.cid_from_sha256(ipfs_sha)
            description = client.cat(ipfs_cid + "/description.txt")
            name = client.cat(ipfs_cid + "/name.txt")
            print(f"Task {i+1})")
            print(" Name:", name.decode("utf-8").strip())
            print(" Description:", description.decode("utf-8").strip())
            print(" Details:", task)
