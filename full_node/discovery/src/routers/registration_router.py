from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from exceptions.http_exceptions import ForbiddenException, UnauthorizedException
from models.responses import RegistrationResponse
from models.requests import RegistrationRequest
from models.did import DIDModel
from services.registration_service import RegistrationService
from dependencies import (
    get_registration_service,
    get_ca_middleware,
    has_ca_access,
    get_did_from_token,
)
from common.middleware.credential_authentication import CredentialAuthenticationMiddleware

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
    ca_middleware: CredentialAuthenticationMiddleware = Depends(get_ca_middleware),
):
    credential = request.credential
    did = request.did
    if credential == {}:
        raise UnauthorizedException("No credential provided")
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
    "/deregister_host",
    status_code=status.HTTP_200_OK,
    response_model=None,
    dependencies=[Depends(has_ca_access)],
)
async def deregister_host(
    didModel: DIDModel,
    registration_service: RegistrationService = Depends(get_registration_service),
    token_did: str = Depends(get_did_from_token),
):
    did = didModel.did
    if did != token_did:
        raise ForbiddenException("DID does not match token")
    registration_service.deregister_host(did)
    # TODO: blacklist token


@registration_router.post("/register_client", response_model=RegistrationResponse)
async def register_client(
    request: RegistrationRequest,
    registration_service: RegistrationService = Depends(get_registration_service),
    ca_middleware: CredentialAuthenticationMiddleware = Depends(get_ca_middleware),
):
    credential = request.credential
    did = request.did
    if credential == {}:
        raise UnauthorizedException("No credential provided")
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
    "/deregister_client",
    status_code=status.HTTP_200_OK,
    response_model=None,
    dependencies=[Depends(has_ca_access)],
)
async def deregister_client(
    didModel: DIDModel,
    registration_service: RegistrationService = Depends(get_registration_service),
    token_did: str = Depends(get_did_from_token),
):
    did = didModel.did
    if did != token_did:
        raise ForbiddenException("DID does not match token")
    registration_service.deregister_client(did)
    # TODO: blacklist token

@registration_router.post("/refresh_access")
async def refresh_access(
    refresh_token: str,
    ca_middleware: CredentialAuthenticationMiddleware = Depends(get_ca_middleware),
):
    access_token = await ca_middleware.refresh_access(refresh_token)
    return {"access_token": access_token, "access_token_type": "bearer"}
