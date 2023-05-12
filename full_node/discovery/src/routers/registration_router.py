from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models.requests import RegistrationRequest
from models.did import DIDModel
from services.registration_service import RegistrationService
from dependencies import (
    get_registration_service,
    get_credential_authentication_middleware,
)
from middleware.credential_authentication import CredentialAuthenticationMiddleware

security = HTTPBearer()

registration_router = APIRouter(
    dependencies=[
        Depends(get_registration_service),
        Depends(get_credential_authentication_middleware),
    ],
    prefix="/registration",
    tags=["registration"],
)


@registration_router.post("/register_host")
async def register_host(
    request: RegistrationRequest,
    registration_service: RegistrationService = Depends(get_registration_service),
    ca_middleware: CredentialAuthenticationMiddleware = Depends(
        get_credential_authentication_middleware
    ),
):
    credential = request.credential
    did = request.did
    if not credential:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No credential provided"
        )
    access_token = await ca_middleware.verify_and_create_vc_access_token(credential)
    registration_service.register_host(did)
    return {"response": "ok", "access_token": access_token, "token_type": "bearer"}


@registration_router.post("/deregister_host")
async def deregister_host(
    didModel: DIDModel,
    registration_service: RegistrationService = Depends(get_registration_service),
    ca_middleware: CredentialAuthenticationMiddleware = Depends(
        get_credential_authentication_middleware
    ),
    authorization: HTTPAuthorizationCredentials = Depends(security),
):
    did = didModel.did
    if not await ca_middleware.has_access(authorization):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    registration_service.deregister_host(did)

    # TODO: blacklist token

    return {"removed": did}


@registration_router.post("/register_user")
async def register_user(
    request: RegistrationRequest,
    registration_service: RegistrationService = Depends(get_registration_service),
    ca_middleware: CredentialAuthenticationMiddleware = Depends(
        get_credential_authentication_middleware
    ),
):
    credential = request.credential
    did = request.did
    if not credential:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No credential provided"
        )
    access_token = await ca_middleware.verify_and_create_vc_access_token(credential)
    registration_service.register_user(did)
    return {"response": "ok", "access_token": access_token, "token_type": "bearer"}


@registration_router.post("/deregister_user")
async def deregister_user(
    didModel: DIDModel,
    registration_service: RegistrationService = Depends(get_registration_service),
    ca_middleware: CredentialAuthenticationMiddleware = Depends(
        get_credential_authentication_middleware
    ),
    authorization: HTTPAuthorizationCredentials = Depends(security),
):
    did = didModel.did
    if not await ca_middleware.has_access(authorization):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    registration_service.deregister_user(did)

    # TODO: blacklist token

    return {"removed": did}
