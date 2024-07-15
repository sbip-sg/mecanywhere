import asyncio
import json
import websockets
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization
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
    peer_public_key = serialization.load_pem_public_key(pub_key_data.encode())
    tmp_ec_key_pair = ec.generate_private_key(ec.SECP384R1())
    shared_secret = tmp_ec_key_pair.exchange(ec.ECDH(), peer_public_key)
    own_public_key_pem = tmp_ec_key_pair.public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
    )

    session_key = HKDF(
        algorithm=hashes.SHA256(),
        length=16,
        salt=None,
        info=b"info",
    ).derive(shared_secret)
    print("session key len: ", len(session_key))

    iv = AES.get_random_bytes(12)
    aes_cipher = AES.new(key=session_key, mode=AES.MODE_GCM, nonce=iv)
    sensitive_data = bytes(input_bytes, "utf-8") + output_key
    padded_sensitive_data = sensitive_data
    encrypted_data = aes_cipher.encrypt(padded_sensitive_data)
    tag = aes_cipher.digest()
    # assemble the message
    encrypted_message = encrypted_data + own_public_key_pem + iv + tag

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
    actor: pymeca.user.MecaUser, task_output: bytes, sgx_ra_round: bool = False
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
    if not sgx_ra_round:
        output_hash = runningTask["outputHash"]
        print("output hash: ", output_hash)
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
    sgx_ra_round=False,
    sgx_output_key=None,
):
    task_output = await websocket.recv()
    print("Task output received.")
    message = verify_and_parse_task_output(
        actor, task_output, sgx_ra_round=sgx_ra_round
    )

    if sgx_output_key is not None:
        message = decrypt_sgx_task_output(message, sgx_output_key)

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
    if use_sgx:
        # prepare the ra input for the enclave
        input_bytes = prepare_input(ipfs_cid, "SGXRAREQUEST", use_sgx=True)
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
            # register the plaintext input hash
            actor.register_tee_task_initial_input(
                task_id, "0x" + keccak(prepare_input(ipfs_cid, input, use_sgx)).hex()
            )
            # prepare input for ra
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
                actor, websocket, task_id, output_folder, sgx_ra_round=True
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
            input_hash = "0x" + keccak(input_bytes).hex()
            actor.register_tee_task_encrypted_input(task_id, input_hash)

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
                    sgx_ra_round=False,
                    sgx_output_key=output_key,
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
    with ipfs_api.ipfshttpclient.connect(
        f"/dns/{ipfs_host}/tcp/{ipfs_port}/http"
    ) as client:
        for i, task in enumerate(tasks):
            ipfs_sha = task["ipfsSha256"]
            ipfs_cid = pymeca.utils.cid_from_sha256(ipfs_sha)
            description = client.cat(ipfs_cid + "/description.txt")
            name = client.cat(ipfs_cid + "/name.txt")
            print(f"Task {i+1})")
            print(" Name:", name.decode("utf-8").strip())
            print(" Description:", description.decode("utf-8").strip())
            print(" Details:", task)
