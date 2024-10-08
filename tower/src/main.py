import secrets
import sys
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
import asyncio
import pymeca

from client_connection_manager import ClientConnectionManager
from host_connection_manager import HostConnectionManager
from dependencies import get_meca_tower


app = FastAPI()

meca_tower = get_meca_tower()

client_manager = ClientConnectionManager()
host_manager = HostConnectionManager()


@app.websocket("/client")
async def websocket_endpoint_client(websocket: WebSocket):
    # try:
    #     while True:
    
    await websocket.accept()

    input_bytes = await websocket.receive_bytes()
    # get the task out of the binary message
    task_id = "0x" + input_bytes[0:32].hex()
    # task_id = "0x" + "0" * 64
    # print(task_id)
    signature = input_bytes[-65:]
    # print(signature)
    verify = pymeca.utils.verify_signature(
        signature_bytes=signature,
        message_bytes=input_bytes[0:-65]
    )

    if not verify:
        await websocket.send_text("Invalid signature")
        return

    user_eth_address = pymeca.utils.get_eth_address_hex_from_signature(
        signature_bytes=signature,
        message_bytes=input_bytes[0:-65]
    )
    user_eth_address = meca_tower.w3.to_checksum_address(user_eth_address)
    blockchain_task = meca_tower.get_running_task(
        task_id=task_id
    )

    if blockchain_task is None:
        await websocket.send_text("Task not found")
        return

    if blockchain_task["owner"] != user_eth_address:
        await websocket.send_text("Unauthorized")
        return

    host_address = blockchain_task["hostAddress"]
    tower_address = blockchain_task["towerAddress"]

    if tower_address != meca_tower.account.address:
        await websocket.send_text("Wrong tower address")
        return

    tower_host = meca_tower.get_my_hosts()
    if host_address not in tower_host:
        await websocket.send_text("Host not found")
        return

    # if not await client_manager.connect(websocket, task_id, host_address):
    #     await websocket.send_text("Task already connected")
    #     return
    await client_manager.connect(websocket, task_id, host_address)

    # output_bytes = input_bytes[32:-65]

    # send the bytes to the host
    # await websocket.send_bytes(output_bytes)
    host_connected = await host_manager.send_input(host_address, input_bytes)
    if not host_connected:
        await websocket.send_text("Host not connected")
        client_manager.disconnect(task_id)
        return

    await websocket.send_text("Task connected")

    try:
        while True:
            await asyncio.sleep(1)  # Keeps the coroutine running
    except asyncio.CancelledError:
        pass
    except WebSocketDisconnect as e:
        print(f"WebSocketDisconnect {e.code}: {e.reason}")
    finally:
        client_manager.disconnect(task_id)


@app.websocket("/host")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    token = secrets.token_bytes(nbytes=32)
    await websocket.send_bytes(token)

    input_bytes = await websocket.receive_bytes()

    host_address = "0x" + input_bytes[0:20].hex()
    host_address = meca_tower.w3.to_checksum_address(host_address)
    signature = input_bytes[-65:]

    verify = pymeca.utils.verify_signature(
        signature_bytes=signature,
        message_bytes=input_bytes[0:20] + token
    )

    if not verify:
        await websocket.send_text("Invalid signature")
        return

    host_ecc_pub_key = pymeca.utils.get_public_key_from_signature(
        signature_bytes=signature,
        message_bytes=input_bytes[0:20] + token
    )
    host_ecc_pub_key_hex = host_ecc_pub_key.to_hex()

    blockchain_host_pub_key = meca_tower.get_host_public_key(
        host_address=host_address
    )

    if host_ecc_pub_key_hex != blockchain_host_pub_key:
        await websocket.send_text("Invalid host encryption public key")
        return

    my_hosts = meca_tower.get_my_hosts()
    if host_address not in my_hosts:
        await websocket.send_text("Host not register with this tower")
        return

    if not await host_manager.connect(websocket, host_address):
        await websocket.send_text("Host already connected")
        return

    await websocket.send_text("Host connected")

    try:
        while True:
            task_output = await websocket.receive_bytes()
            task_id = "0x" + task_output[0:32].hex()
            signature = task_output[-65:]
            verify = pymeca.utils.verify_signature_pub_key(
                signature_bytes=signature,
                message_bytes=task_output[0:-65],
                public_key=host_ecc_pub_key
            )
            if not verify:
                await websocket.send_text("Invalid signature")
                continue
            task_connected = await client_manager.send_output(
                task_id=task_id,
                host_address=host_address,
                output_bytes=task_output
            )
            if not task_connected:
                await websocket.send_text("Task not connected")
                continue
            await websocket.send_text("Task output sent")
    except asyncio.CancelledError:
        pass
    except WebSocketDisconnect as e:
        print(f"WebSocketDisconnect {e.code}: {e.reason}")
    finally:
        host_manager.disconnect(host_address)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI WebSocket server."}


async def run_websocket_server(port: int = 7777):
    import uvicorn
    config = uvicorn.Config(
        "main:app",
        host="0.0.0.0",
        port=port,
        forwarded_allow_ips="*",
        ws_ping_timeout=60,
        log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    with open("openapi.json", "w") as f:
        json.dump(app.openapi(), f)
    try:
        asyncio.run(run_websocket_server(port=int(sys.argv[1])))
    except KeyboardInterrupt:
        print("Exiting")
        exit(0)

