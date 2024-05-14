import asyncio
import inspect
import json
import os
import sys
from fastapi import FastAPI, HTTPException, Request
import pymeca
from dotenv import load_dotenv

from web3 import Web3

load_dotenv()

BLOCKCHAIN_URL = os.getenv("MECA_BLOCKCHAIN_RPC_URL", "http://localhost:8545")
DAO_ADDRESS = pymeca.dao.get_DAO_ADDRESS()

app = FastAPI()
actor = None

@app.get('/')
def home():
    return "Meca Server"

@app.post('/{function_name}')
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


@app.post('/init_actor/{actor_name}')
def init_actor(actor_name: str):
    global actor
    if actor is not None:
        raise HTTPException(status_code=400, detail="Actor already initialized")
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

@app.get('/get_account')
def get_account():
    if actor is None:
        init_actor("user")
    return actor.account.address

@app.get('/cid_from_sha256/{sha256}')
def cid_from_sha256(sha256: str):
    return pymeca.utils.cid_from_sha256(sha256)

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
