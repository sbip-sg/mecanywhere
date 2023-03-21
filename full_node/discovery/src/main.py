from contract import DiscoveryContract, EthDiscoveryContract
from config import Config
from ip_assign_strategy import RoundRobinAssignStrategy, IpAssignStrategy
from fastapi import FastAPI, Depends, Request, Query, Response, status
from fastapi.middleware.cors import CORSMiddleware
from common import get_current_timestamp
from cleanup_task import CleanupTask

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"],
)

@app.middleware("http")
async def add_credentials_authentication(request: Request, call_next):
    if "Authorization" not in request.headers:
        return Response("No authorization.", status_code=status.HTTP_403_FORBIDDEN)
    auth = request.headers["Authorization"]
    if False: # TODO: call DID service to verify VC
        return Response("Authentication failed.", status_code=status.HTTP_401_UNAUTHORIZED)
    response = await call_next(request)
    return response

async def get_discovery_contract() -> DiscoveryContract:
    global _discovery_contract
    return _discovery_contract


async def get_ip_assigner() -> IpAssignStrategy:
    global _ip_assigner
    return _ip_assigner


@app.on_event("startup")
async def start_up():
    global _discovery_contract
    global _ip_assigner
    global _cleanup_task

    config = Config("../config.json")

    _discovery_contract = EthDiscoveryContract(
        abi_path=config.get_abi_path(),
        contract_address=config.get_contract_address(),
        url=config.get_contract_url(),
        transaction_gas=config.get_transaction_gas())

    _ip_assigner = RoundRobinAssignStrategy(_discovery_contract)

    _cleanup_task = CleanupTask(
        config.get_cleanup_interval(),
        config.get_cleanup_expire(),
        _discovery_contract,
        _ip_assigner)
    _cleanup_task.run()


@app.get("/register_host")
async def register_host(request: Request, contract: DiscoveryContract = Depends(get_discovery_contract)):
    ip_address = request.client.host
    contract.set_ip_address_timestamp(ip_address, get_current_timestamp())
    return {"response": "ok"}


@app.get("/assign_host")
async def assign_host(ip_assigner: IpAssignStrategy = Depends(get_ip_assigner)):
    try:
        ip_address = ip_assigner.assign()
        return {"ip_address": ip_address}
    except:
        return {"ip_address": ""}


@app.post("/heartbeat")
async def heartbeat(request: Request, contract: DiscoveryContract = Depends(get_discovery_contract)):
    ip_address = request.client.host
    contract.set_ip_address_timestamp(
        ip_address=ip_address, timestamp=get_current_timestamp())
    return {"response": "ok"}


# for testing purposes
@app.get("/deregister_host")
async def deregister_host(ip: str = Query(None), contract: DiscoveryContract = Depends(get_discovery_contract)):
    contract.removeIpAddress(ip)
    return {"removed": ip}
