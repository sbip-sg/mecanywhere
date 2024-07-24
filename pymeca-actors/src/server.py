import asyncio
import inspect
import json
import os
import pathlib
import sys
import threading
from fastapi import FastAPI, HTTPException, Request
import pymeca
from dotenv import load_dotenv
from functions.user_functions import send_task_on_blockchain 
from functions.host_functions import TaskThread
from pydantic import BaseModel

from web3 import Web3

load_dotenv()

BLOCKCHAIN_URL = os.getenv("MECA_BLOCKCHAIN_RPC_URL", "http://localhost:8545")
TASK_EXECUTOR_URL = os.getenv("MECA_TASK_EXECUTOR_URL", "http://host.docker.internal:2591")
DAO_ADDRESS = pymeca.dao.get_DAO_ADDRESS()
HOST_ENCRYPTION_PRIVATE_KEY = os.getenv("MECA_HOST_ENCRYPTION_PRIVATE_KEY", None)
IPFS_HOST = os.getenv("MECA_IPFS_HOST", "host.docker.internal")
IPFS_PORT = os.getenv("MECA_IPFS_PORT", "5001")

CONTAINER_NAME_LIMIT = 10
OUTPUT_FOLDER = pathlib.Path("./build")

app = FastAPI()
actor = None
web3 = None

@app.get('/')
def home():
    return "Meca Server"

@app.post('/exec/{function_name}')
async def entry_point(function_name: str, request: Request = None):
    if actor is None:
        raise HTTPException(status_code=400, detail="Actor not initialized")
    func = getattr(actor, function_name, None)
    if func is None:
        raise HTTPException(status_code=404, detail=f"Function {function_name} not found")
    if request is None or await request.body() == b'':
        args = {}
    else:
        args = await request.json()
    try:
        is_coroutine = inspect.iscoroutinefunction(func)
        if is_coroutine:
            return await func(**args)
        else:
            return func(**args)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post('/init_actor/{actor_name}', response_model=bool)
def init_actor(actor_name: str):
    global actor
    global web3
    try:
        web3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))
        if actor_name == "host":
            private_key = os.getenv("MECA_HOST_PRIVATE_KEY", None)
            actor = pymeca.host.MecaHost(web3, private_key, DAO_ADDRESS)
        elif actor_name == "tower":
            private_key = os.getenv("MECA_TOWER_PRIVATE_KEY", None)
            actor = pymeca.tower.MecaTower(web3, private_key, DAO_ADDRESS)
        elif actor_name == "user":
            private_key = os.getenv("MECA_USER_PRIVATE_KEY", None)
            actor = pymeca.user.MecaUser(web3, private_key, DAO_ADDRESS)
        elif actor_name == "task_dev":
            private_key = os.getenv("MECA_DEV_PRIVATE_KEY", None)
            actor = pymeca.task.MecaTaskDeveloper(web3, private_key, DAO_ADDRESS)
        else:
            raise ValueError(f"Invalid actor: {actor_name}")
        return True
    except ValueError as e:
        return str(e)
    
@app.post('/close_actor')
def close_actor():
    global actor
    if actor is None:
        raise HTTPException(status_code=400, detail="Actor not initialized")
    actor = None
    return True

@app.get('/get_account', response_model=str)
def get_account():
    if actor is None:
        raise HTTPException(status_code=400, detail="Actor not initialized")
    return actor.account.address

@app.get('/cid_from_sha256/{sha256}', response_model=str)
def cid_from_sha256(sha256: str):
    return pymeca.utils.cid_from_sha256(sha256)

class SendTaskOnBlockchainArgs(BaseModel):
    ipfs_sha256: str
    host_address: str
    tower_address: str
    input_hash: str
    use_sgx: bool = False

@app.post('/send_task_on_blockchain')
async def send_task(request: SendTaskOnBlockchainArgs):
    if actor is None:
        raise HTTPException(status_code=400, detail="Actor not initialized")
    return await send_task_on_blockchain(
        actor,
        request.ipfs_sha256,
        request.host_address,
        request.tower_address,
        request.input_hash,
        OUTPUT_FOLDER,
        request.use_sgx
    )

class WaitForTaskArgs(BaseModel):
    tower_address: str

@app.post('/wait_for_task')
async def wait_for_my_task(request: WaitForTaskArgs):
    if actor is None:
        raise HTTPException(status_code=400, detail="Actor not initialized")
    kill_event = threading.Event()
    task_thread = TaskThread(kill_event, args=(
        actor,
        request.tower_address,
        HOST_ENCRYPTION_PRIVATE_KEY,
        CONTAINER_NAME_LIMIT,
        TASK_EXECUTOR_URL,
        IPFS_HOST,
        IPFS_PORT,
    ))
    task_thread.start()

@app.get('/get_block_timestamp/{block_number}', response_model=int)
async def getBlockTimestamp(block_number: int):
    if web3 is None:
        raise HTTPException(status_code=400, detail="Service not initialized")
    return web3.eth.get_block(block_number).timestamp

async def run_websocket_server(port: int = 9999):
    import uvicorn
    config = uvicorn.Config(
        "server:app",
        host="0.0.0.0",
        port=port,
        forwarded_allow_ips="*",
        reload=True,
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
