import threading
from config import Config
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from services.result_queue import ResultQueue
from routers.account_creation_router import account_creation_router
from routers.login_router import login_router
from routers.registration_router import registration_router
from routers.offload_router import offload_router
from routers.monitoring_router import monitoring_router
from dependencies import has_ca_access, get_config


app = FastAPI(title="Full Node - Discovery")
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"],
)
app.include_router(registration_router)
app.include_router(account_creation_router)
app.include_router(login_router)
app.include_router(offload_router, dependencies=[Depends(has_ca_access)])
app.include_router(monitoring_router, dependencies=[Depends(has_ca_access)])


result_queue = None
queue_thread = None

def start_consuming(config: Config) -> None:
    global result_queue
    result_queue = ResultQueue(config)
    print("Starting relayer")
    result_queue.start_consumer()
    print("Relayer stopped")


@app.on_event("startup")
async def start_up():
    global result_queue, queue_thread
    queue_thread = threading.Thread(target=start_consuming, args=([get_config()]))
    queue_thread.start()


@app.on_event("shutdown")
async def shut_down():
    global result_queue, queue_thread
    if result_queue is not None:
        result_queue.stop()
    if queue_thread is not None:
        queue_thread.join()

