from contextlib import asynccontextmanager
import json
from multiprocessing import Process
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers.authentication_router import authentication_router
from services.message_queue.result_queue import ResultQueue
from routers.offload_router import offload_router
from dependencies import get_tower_contract, has_ca_access, get_config, get_cache


result_queue = None
queue_process = None


def start_consuming() -> None:
    global result_queue
    config = get_config()
    cache = get_cache(config)
    with ResultQueue(config, cache) as result_queue:
        print("Starting relayer", flush=True)
        result_queue.start_consumer()
        print("Relayer stopped", flush=True)


async def start_up():
    global result_queue, queue_process

    queue_process = Process(target=start_consuming)
    queue_process.start()

    contract = get_tower_contract(get_config())
    contract.registerTower(100, "http://localhost:7000", 100, 0)    


async def shut_down():
    global result_queue, queue_process
    if result_queue is not None:
        result_queue.stop()
    if queue_process is not None:
        queue_process.join()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_up()
    try:
        yield
    finally:
        await shut_down()


app = FastAPI(title="Full Node - Discovery", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"],
)
app.include_router(authentication_router)
app.include_router(offload_router, dependencies=[Depends(has_ca_access)])

with open("openapi.json", "w") as f:
    json.dump(app.openapi(), f)
