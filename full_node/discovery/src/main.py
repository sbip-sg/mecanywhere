from contract import DiscoveryContract, EthDiscoveryContract
from config import Config
from ip_assign_strategy import RoundRobinAssignStrategy, IpAssignStrategy
from fastapi import FastAPI, Depends, Request, Query
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"],
)

_discovery_contract = None
_ip_assigner = None


async def get_discovery_contract() -> DiscoveryContract:
    global _discovery_contract
    return _discovery_contract


async def get_ip_assigner() -> IpAssignStrategy:
    global _ip_assigner
    return _ip_assigner


def get_current_timestamp() -> int:
    return int(datetime.utcnow().timestamp())


@app.on_event("startup")
async def start_up():
    global _discovery_contract
    global _ip_assigner

    config = Config("../config.json")

    _discovery_contract = EthDiscoveryContract(
        abi_path=config.get_abi_path(),
        contract_address=config.get_contract_address(),
        url=config.get_contract_url(),
        transaction_gas=config.get_transaction_gas())

    _ip_assigner = RoundRobinAssignStrategy(_discovery_contract)


@app.get("/register_ip")
async def register_ip(request: Request, contract: DiscoveryContract = Depends(get_discovery_contract)):
    ip_address = request.client.host
    contract.set_ip_address_timestamp(ip_address, get_current_timestamp())
    return {"response": "ok"}


@app.get("/assign_ip")
async def assign_ip(ip_assigner: IpAssignStrategy = Depends(get_ip_assigner)):
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
@app.get("/remove_ip")
async def remove_ip(ip: str = Query(None), contract: DiscoveryContract = Depends(get_discovery_contract)):
    contract.removeIpAddress(ip)
    return {"removed": ip}
