from fastapi import FastAPI, Depends
from message import ComputeResultRequest, UpdateResultRequest, ComputeRequest
from compute_task import ComputeTask
from heartbeat_task import HeartbeatTask
from result import InMemoryResultMapping, ResultMapping
from fastapi.middleware.cors import CORSMiddleware
from config import Config


app = FastAPI()

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

    _result_mapping = InMemoryResultMapping()
    _compute_task = ComputeTask(result_mapping=_result_mapping)

    _compute_task.start()
    config = Config('../config.json')
    _heartbeat_task = HeartbeatTask(
        url=config.get_heartbeat_url(), periodic_interval=config.get_heartbeat_interval_sec())
    _heartbeat_task.start()


@app.post("/compute")
async def compute(req: ComputeRequest, task: ComputeTask = Depends(get_compute_task)):
    task.enqueue(req)
    return {"response": "ok"}


@app.post("/get_result")
async def get_result(req: ComputeResultRequest, result_mapping: ResultMapping = Depends(get_result_mapping)):
    result = result_mapping.get(req.id)
    return {"result": result}


@app.post("/internel_update_result")
async def update_result(req: UpdateResultRequest, result_mapping: ResultMapping = Depends(get_result_mapping)):
    result_mapping.set(req.id, req.result)
    return {"response": "ok"}
