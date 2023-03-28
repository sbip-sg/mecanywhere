from config import Config
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
import aiohttp
from contract import DiscoveryContract, EthDiscoveryContract
from tasks.cleanup_task import CleanupTask
from middleware.credential_authentication import CredentialAuthenticationMiddleware
from services.registration_service import RegistrationService
from services.assignment_service import AssignmentService
from services.monitoring_service import MonitoringService


app = FastAPI()
config = Config("../config.json")
session = aiohttp.ClientSession()


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"],
)
app.add_middleware(CredentialAuthenticationMiddleware, config=config, session=session)


async def get_discovery_contract() -> DiscoveryContract:
    return _discovery_contract

async def get_assignment_service() -> AssignmentService:
    return _assignment_service

async def get_registration_service() -> RegistrationService:
    return _registration_service

async def get_monitoring_service() -> MonitoringService:
    return _monitoring_service


@app.on_event("startup")
async def start_up():
    global _discovery_contract
    global _assignment_service
    global _registration_service
    global _monitoring_service
    global _cleanup_task

    _discovery_contract = EthDiscoveryContract(
        abi_path=config.get_abi_path(),
        contract_address=config.get_contract_address(),
        url=config.get_contract_url(),
        transaction_gas=config.get_transaction_gas(),
    )

    _assignment_service = AssignmentService(_discovery_contract)
    _registration_service = RegistrationService(_discovery_contract)
    _monitoring_service = MonitoringService(_discovery_contract)

    _cleanup_task = CleanupTask(
        config.get_cleanup_interval(),
        config.get_cleanup_expire(),
        _discovery_contract,
        _assignment_service,
    )
    _cleanup_task.run()


@app.get("/register_host")
async def register_host(
    request: Request,
    registration_service: RegistrationService = Depends(get_registration_service),
):
    ip_address = request.client.host
    registration_service.register_host(ip_address)
    return {"response": "ok"}


@app.get("/assign_host")
async def assign_host(
    assignment_service: AssignmentService = Depends(get_assignment_service),
):
    ip_address = assignment_service.assign()
    return {"ip_address": ip_address}


@app.post("/heartbeat")
async def heartbeat(
    request: Request,
    monitoring_service: MonitoringService = Depends(get_monitoring_service),
):
    ip_address = request.client.host
    monitoring_service.heartbeat(ip_address)
    return {"response": "ok"}


@app.get("/deregister_host")
async def deregister_host(
    request: Request,
    registration_service: RegistrationService = Depends(get_registration_service),
):
    ip_address = request.client.host
    registration_service.deregister_host(ip_address)
    return {"removed": ip_address}
