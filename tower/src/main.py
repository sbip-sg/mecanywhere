from contextlib import asynccontextmanager
from fastapi.websockets import WebSocketState
from pymeca.tower import MecaTower
from fastapi import FastAPI, HTTPException, WebSocket, Request, Depends, WebSocketDisconnect, status
import json
import asyncio

from dependencies import get_meca_tower
from websocket_manager import WebsocketManager


manager = WebsocketManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await manager.shutdown()    


app = FastAPI(lifespan=lifespan)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str,
    meca_tower: MecaTower = Depends(get_meca_tower)
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


@app.post("/send_message")
async def send_message(
    request: Request,
    meca_tower: MecaTower = Depends(get_meca_tower)
):
    data = await request.json()
    task_id = data["taskId"]
    # Check if the task is submitted on the blockchain
    running_task = meca_tower.get_running_task(task_id)
    if running_task is None:
        return {"error": f"Task {task_id} not found."}
    print("Running task found.")

    target_client_id = running_task["hostAddress"]
    try:
        await manager.send_message(target_client_id, json.dumps(data))
        return await manager.receive_message(target_client_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Client not found.")


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI WebSocket server."}
