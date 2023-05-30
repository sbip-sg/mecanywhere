from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models.responses import RegistrationResponse
from models.requests import RegistrationRequest
from models.did import DIDModel
from services.registration_service import RegistrationService
from dependencies import (
    get_registration_service,
    get_ca_middleware,
)
from middleware.credential_authentication import CredentialAuthenticationMiddleware

security = HTTPBearer()

registration_router = APIRouter(
    dependencies=[
        Depends(get_registration_service),
        Depends(get_ca_middleware),
    ],
    prefix="/registration",
    tags=["registration"],
)


@registration_router.post("/register_host", response_model=RegistrationResponse)
async def register_host(
    request: RegistrationRequest,
    registration_service: RegistrationService = Depends(get_registration_service),
    ca_middleware: CredentialAuthenticationMiddleware = Depends(
        get_ca_middleware
    ),
):
    credential = request.credential
    did = request.did
    if credential == {}:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No credential provided"
        )
    (access_token, refresh_token) = await ca_middleware.verify_and_create_tokens(
        did, credential
    )
    registration_service.register_host(did)
    return {
        "access_token": access_token,
        "access_token_type": "bearer",
        "refresh_token": refresh_token,
        "refresh_token_type": "bearer",
    }


@registration_router.post(
    "/deregister_host", status_code=status.HTTP_200_OK, response_model=None
)
async def deregister_host(
    didModel: DIDModel,
    registration_service: RegistrationService = Depends(get_registration_service),
    ca_middleware: CredentialAuthenticationMiddleware = Depends(
        get_ca_middleware
    ),
    authorization: HTTPAuthorizationCredentials = Depends(security),
):
    did = didModel.did
    if not await ca_middleware.has_access(authorization):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    registration_service.deregister_host(did)
    # TODO: blacklist token


@registration_router.post("/register_client", response_model=RegistrationResponse)
async def register_client(
    request: RegistrationRequest,
    registration_service: RegistrationService = Depends(get_registration_service),
    ca_middleware: CredentialAuthenticationMiddleware = Depends(
        get_ca_middleware
    ),
):
    credential = request.credential
    did = request.did
    if credential == {}:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No credential provided"
        )
    (access_token, refresh_token) = await ca_middleware.verify_and_create_tokens(
        did, credential
    )
    registration_service.register_client(did)
    return {
        "access_token": access_token,
        "access_token_type": "bearer",
        "refresh_token": refresh_token,
        "refresh_token_type": "bearer",
    }


@registration_router.post(
    "/deregister_client", status_code=status.HTTP_200_OK, response_model=None
)
async def deregister_client(
    didModel: DIDModel,
    registration_service: RegistrationService = Depends(get_registration_service),
    ca_middleware: CredentialAuthenticationMiddleware = Depends(
        get_ca_middleware
    ),
    authorization: HTTPAuthorizationCredentials = Depends(security),
):
    did = didModel.did
    if not await ca_middleware.has_access(authorization):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    registration_service.deregister_client(did)
    # TODO: blacklist token


@registration_router.post("/refresh_access")
async def refresh_access(refresh_token: str, ca_middleware: CredentialAuthenticationMiddleware = Depends(
        get_ca_middleware
    ),):
    access_token = await ca_middleware.refresh_access(refresh_token)
    return {"access_token": access_token, "access_token_type": "bearer"}
