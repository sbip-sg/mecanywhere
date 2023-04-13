from config import Config
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import aiohttp
from contract import EthDiscoveryContract
from tasks.cleanup_task import CleanupTask
from middleware.credential_authentication import CredentialAuthenticationMiddleware
from services.registration_service import RegistrationService
from services.assignment_service import AssignmentService
from services.monitoring_service import MonitoringService
from routers.registration_router import registration_router
from routers.assignment_router import assignment_router
from routers.monitoring_router import monitoring_router


config = Config("../config.json")
session = aiohttp.ClientSession()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"],
)
app.include_router(registration_router)
ca_middleware = CredentialAuthenticationMiddleware(app, config, session)
app.include_router(assignment_router, dependencies=[Depends(ca_middleware.has_access)])
app.include_router(monitoring_router, dependencies=[Depends(ca_middleware.has_access)])


@app.on_event("startup")
async def start_up():
    global discovery_contract
    global assignment_service
    global registration_service
    global monitoring_service
    global _cleanup_task

    discovery_contract = EthDiscoveryContract(
        abi_path=config.get_abi_path(),
        contract_address=config.get_contract_address(),
        url=config.get_contract_url(),
        transaction_gas=config.get_transaction_gas(),
    )

    assignment_service = AssignmentService(discovery_contract)
    registration_service = RegistrationService(discovery_contract)
    monitoring_service = MonitoringService(discovery_contract)

    _cleanup_task = CleanupTask(
        config.get_cleanup_interval(),
        config.get_cleanup_expire(),
        discovery_contract,
        assignment_service,
    )
    _cleanup_task.run()
