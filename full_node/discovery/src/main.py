import threading
from config import Config
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from services.result_relayer import ResultRelayer
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


relayer = None
relayer_thread = None

def start_relaying(config: Config) -> None:
    with ResultRelayer(config) as relayer:
        print("Starting relayer")
        relayer.start_relayer()
        print("Relayer stopped")


@app.on_event("startup")
async def start_up():
    relayer_thread = threading.Thread(target=start_relaying, args=([get_config()]))
    relayer_thread.start()


@app.on_event("shutdown")
async def shut_down():
    if relayer is not None:
        relayer.stop()
    if relayer_thread is not None:
        relayer_thread.join()

