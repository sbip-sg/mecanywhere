from contextlib import asynccontextmanager
from fastapi.websockets import WebSocketState
from pymeca.tower import MecaTower
from fastapi import (
    FastAPI,
    HTTPException,
    WebSocket,
    Depends,
    WebSocketDisconnect,
    status,
)
import json
import asyncio
import hashlib

from dependencies import get_meca_tower
from models.requests import SendMessageRequest
from models.responses import SendMessageResponse
from websocket_manager import WebsocketManager

from store import MecaLocalFsStore

manager = WebsocketManager()
store = MecaLocalFsStore()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await manager.shutdown()
    await store.close()


app = FastAPI(lifespan=lifespan)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str,
    meca_tower: MecaTower = Depends(get_meca_tower),
):
    # check if the client is a host on the tower
    if client_id not in meca_tower.get_my_hosts():
        return await websocket.close()
    await manager.accept(websocket, client_id)

    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            await asyncio.sleep(1)  # Keeps the coroutine running
    except asyncio.CancelledError:
        pass
    except WebSocketDisconnect as e:
        print(f"WebSocketDisconnect {e.code}: {e.reason}")
    finally:
        manager.disconnect(client_id)


@app.post("/send_message", response_model=SendMessageResponse)
async def send_message(
    request: SendMessageRequest, meca_tower: MecaTower = Depends(get_meca_tower)
):
    task_id = request.taskId
    # Check if the task is submitted on the blockchain
    running_task = meca_tower.get_running_task(task_id)
    if running_task is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Task not found."
        )
    print("Running task found.")

    target_client_id = running_task["hostAddress"]
    # check if we already have the result
    try:
        result = store.retrieve("results", task_id)
        return json.loads(result)
    except store.MecaStoreError:
        pass

    try:
        await manager.send_message(target_client_id, request.model_dump_json())
        reply = await manager.receive_message(target_client_id)

        # [TODO] check if the reply hash matches the host uploaded result hash on-chain
        reply_hash = hashlib.sha256(reply.encode("utf-8")).hexdigest()

        # generate acknowledgement (maybe include a signed digest)
        # [TODO] here the block number is a TTL for cleanup at tower. Now no cleanup yet.
        store.store("results", task_id, reply, running_task["blockno"])
        await manager.send_message(target_client_id, json.dumps({"ack": reply_hash}))

        return json.loads(reply)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Client not found."
        )


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI WebSocket server."}


with open("openapi.json", "w") as f:
    json.dump(app.openapi(), f)
