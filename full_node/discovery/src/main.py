import asyncio
from contextlib import asynccontextmanager
from multiprocessing import Process, Event
import signal
import threading
from config import Config
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers.authentication_router import authentication_router
from services.message_queue.result_queue import ResultQueue
from routers.account_creation_router import account_creation_router
from routers.login_router import login_router
from routers.registration_router import registration_router
from routers.offload_router import offload_router
from routers.monitoring_router import monitoring_router
from dependencies import has_ca_access, get_config, get_redis_client


result_queue = None
queue_process = None


def start_consuming(config: Config) -> None:
    global result_queue
    cache = get_redis_client(config)
    with ResultQueue(config, cache) as result_queue:
        print("Starting relayer", flush=True)
        result_queue.start_consumer()
        print("Relayer stopped", flush=True)


async def start_up():
    global result_queue, queue_process

    config = get_config()
    queue_process = Process(target=start_consuming, args=(config,))
    queue_process.start()


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
app.include_router(registration_router, dependencies=[Depends(has_ca_access)])
app.include_router(account_creation_router)
app.include_router(login_router)
app.include_router(offload_router, dependencies=[Depends(has_ca_access)])
app.include_router(monitoring_router, dependencies=[Depends(has_ca_access)])
