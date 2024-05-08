import asyncio
import json
import sys
from fastapi import FastAPI, HTTPException, Request

from mock_host import MecaHostCLI
from mock_tower import MecaTowerCLI
from mock_user import MecaUserCLI
from mock_task_dev import TaskDeveloperCLI

app = FastAPI()
actor = None

@app.get('/')
def home():
    return "Meca Server"

@app.post('/{function_name}')
async def entry_point(function_name: str, request: Request = None):
    if actor is None:
        raise HTTPException(status_code=400, detail="Actor not initialized")
    func = actor.get_method(function_name)
    if func is None:
        raise HTTPException(status_code=404, detail=f"Function {function_name} not found")
    if request is None or await request.body() == b'':
        args = {}
    else:
        args = await request.json()
    try:
        return await actor.run_func(func, args)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post('/init_actor/{actor_name}')
def init_actor(actor_name: str):
    global actor
    if actor is not None:
        raise HTTPException(status_code=400, detail="Actor already initialized")
    try:
        if actor_name == "host":
            actor = MecaHostCLI()
        elif actor_name == "tower":
            actor = MecaTowerCLI()
        elif actor_name == "user":
            actor = MecaUserCLI()
        elif actor_name == "task_dev":
            actor = TaskDeveloperCLI()
        else:
            raise ValueError(f"Invalid actor: {actor_name}")
        return list(actor.name_to_child_method.keys())
    except ValueError as e:
        return str(e)

@app.get('/get_account')
def get_account():
    if actor is None:
        # using an arbitrary actor to get the address
        return MecaUserCLI().account.address
    return actor.account.address

async def run_websocket_server(port: int = 9999):
    import uvicorn
    config = uvicorn.Config(
        "server:app",
        host="0.0.0.0",
        port=port,
        forwarded_allow_ips="*",
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
