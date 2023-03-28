from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.message import ComputeResultRequest, UpdateResultRequest, ComputeRequest
from models.result import InMemoryResultMapping, ResultMapping
from tasks.compute_task import ComputeTask
from tasks.heartbeat_task import HeartbeatTask
from config import Config
import aiohttp


app = FastAPI()
config = Config("../config.json")
session_headers = {"Authorization": ""}
session = aiohttp.ClientSession(headers=session_headers)


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

    async with session.get(config.get_register_host_url()) as result:
        if result.status == status.HTTP_200_OK:
            _result_mapping = InMemoryResultMapping()
            _compute_task = ComputeTask(result_mapping=_result_mapping)

            _compute_task.start()

            _heartbeat_task = HeartbeatTask(
                url=config.get_heartbeat_url(),
                periodic_interval=config.get_heartbeat_interval_sec(),
                session=session,
            )

            await _heartbeat_task.start()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to register as host.",
            )


@app.on_event("shutdown")
async def shut_down():
    await _heartbeat_task.terminate()
    await _compute_task.terminate()
    async with session.get(config.get_deregister_host_url()) as r:
        pass
    await session.close()


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


@app.post("/internel_update_result")
async def update_result(
    req: UpdateResultRequest,
    result_mapping: ResultMapping = Depends(get_result_mapping),
):
    result_mapping.set(req.id, req.result)
    return {"response": "ok"}
