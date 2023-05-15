from config import Config
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import aiohttp
from contract import EthDiscoveryContract
from middleware.credential_authentication import CredentialAuthenticationMiddleware
from services.account_creation_service import AccountCreationService
from services.login_service import LoginService
from services.registration_service import RegistrationService
from services.assignment_service import AssignmentService
from services.monitoring_service import MonitoringService
from routers.account_creation_router import account_creation_router
from routers.login_router import login_router
from routers.registration_router import registration_router
from routers.assignment_router import assignment_router
from routers.monitoring_router import monitoring_router


config = Config("../config.json", "../../config.json")
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
app.include_router(account_creation_router)
app.include_router(login_router)
ca_middleware = CredentialAuthenticationMiddleware(app, config, session)
app.include_router(assignment_router, dependencies=[Depends(ca_middleware.has_access)])
app.include_router(monitoring_router, dependencies=[Depends(ca_middleware.has_access)])


@app.on_event("startup")
async def start_up():
    global discovery_contract
    global assignment_service
    global registration_service
    global monitoring_service
    global account_creation_service
    global login_service


    discovery_contract = EthDiscoveryContract(
        abi_path=config.get_abi_path(),
        contract_address=config.get_contract_address(),
        url=config.get_contract_url(),
    )

    assignment_service = AssignmentService(discovery_contract)
    registration_service = RegistrationService(discovery_contract)
    monitoring_service = MonitoringService(discovery_contract)
    account_creation_service = AccountCreationService()
    login_service = LoginService()
