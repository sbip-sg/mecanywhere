from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.message import ComputeResultRequest, UpdateResultRequest, ComputeRequest
from models.result import InMemoryResultMapping, ResultMapping
from tasks.compute_task import ComputeTask
from tasks.heartbeat_task import HeartbeatTask
from config import Config
import aiohttp
from credential_example import credential_example

app = FastAPI()
config = Config("../config.json")
headers = {"Authorization": "Bearer "}
session = aiohttp.ClientSession(headers=headers)


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"],
)


async def get_result_mapping():
    global _result_mapping
    return _result_mapping


async def get_compute_task():
    global _compute_task
    return _compute_task


@app.on_event("startup")
async def start_up():
    global _result_mapping
    global _compute_task
    global _heartbeat_task
    global _registered_as_host
    global _registered_as_user
    _registered_as_host = False
    _registered_as_user = False


@app.on_event("shutdown")
async def shut_down():
    if _heartbeat_task is not None:
        await _heartbeat_task.terminate()
    if _compute_task is not None:
        await _compute_task.terminate()
    if _registered_as_host:
        await session.get(config.get_deregister_host_url())
    if _registered_as_user:
        await session.get(config.get_deregister_user_url())
    await session.close()


@app.post("/register_host")
async def register_host(credentials: dict):
    global _result_mapping
    global _compute_task
    global _heartbeat_task
    global _registered_as_host
    async with session.post(
        config.get_register_host_url(), json=credentials
    ) as registration_res:
        if registration_res.status == status.HTTP_200_OK:
            _registered_as_host = True
            _result_mapping = InMemoryResultMapping()
            _compute_task = ComputeTask(result_mapping=_result_mapping)

            _compute_task.start()

            _heartbeat_task = HeartbeatTask(
                url=config.get_heartbeat_url(),
                periodic_interval=config.get_heartbeat_interval_sec(),
                session=session,
            )

            await _heartbeat_task.start()

            registration_res_json = await registration_res.json()
            access_token = registration_res_json["access_token"]
            session.headers["Authorization"] = f"Bearer {access_token}"
            return registration_res_json
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to register as host.",
            )


@app.get("/deregister_host")
async def register_host():
    global _registered_as_host
    async with session.get(config.get_deregister_host_url()) as deregistration_res:
        _registered_as_host = False
        await _heartbeat_task.terminate()
        await _compute_task.terminate()
        return await deregistration_res.json()


@app.post("/compute")
async def compute(req: ComputeRequest, task: ComputeTask = Depends(get_compute_task)):
    task.enqueue(req)
    return {"response": "ok"}


@app.post("/get_result")
async def get_result(
    req: ComputeResultRequest,
    result_mapping: ResultMapping = Depends(get_result_mapping),
):
    result = result_mapping.get(req.id)
    return {"result": result}


@app.post("/register_user")
async def register_user(credentials: dict):
    global _registered_as_user
    async with session.post(
        config.get_register_user_url(), json=credentials
    ) as registration_res:
        if registration_res.status == status.HTTP_200_OK:
            _registered_as_user = True
            registration_res_json = await registration_res.json()
            access_token = registration_res_json["access_token"]
            session.headers["Authorization"] = f"Bearer {access_token}"
            return registration_res_json
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to register as user.",
            )


@app.get("/deregister_user")
async def register_user():
    global _registered_as_user
    async with session.get(config.get_deregister_user_url()) as deregistration_res:
        _registered_as_user = False
        return await deregistration_res.json()


@app.get("/get_host")
async def get_host():
    async with session.get(config.get_assign_host_url()) as res:
        return await res.json()
