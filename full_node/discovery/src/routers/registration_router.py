from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
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
)

@registration_router.post("/register_host")
async def register_host(
    request: Request,
    registration_service: RegistrationService = Depends(get_registration_service),
    ca_middleware: CredentialAuthenticationMiddleware = Depends(get_credential_authentication_middleware),
):
    credential = await request.json()
    if not credential:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No credential provided")
    access_token = await ca_middleware.verify_and_create_vc_access_token(credential)
    ip_address = request.client.host
    registration_service.register_host(ip_address)
    return {"response": "ok", "access_token": access_token, "token_type": "bearer"}


@registration_router.get("/deregister_host")
async def deregister_host(
    request: Request,
    registration_service: RegistrationService = Depends(get_registration_service),
    ca_middleware: CredentialAuthenticationMiddleware = Depends(get_credential_authentication_middleware),
    authorization: HTTPAuthorizationCredentials = Depends(security)
):
    if not await ca_middleware.has_access(authorization):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    ip_address = request.client.host
    registration_service.deregister_host(ip_address)

    # TODO: blacklist token

    return {"removed": ip_address}


@registration_router.post("/register_user")
async def register_user(
    request: Request,
    registration_service: RegistrationService = Depends(get_registration_service),
    ca_middleware: CredentialAuthenticationMiddleware = Depends(get_credential_authentication_middleware),
):
    credential = await request.json()
    if not credential:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No credential provided")
    access_token = await ca_middleware.verify_and_create_vc_access_token(credential)
    ip_address = request.client.host
    registration_service.register_user(ip_address)
    return {"response": "ok", "access_token": access_token, "token_type": "bearer"}


@registration_router.get("/deregister_user")
async def deregister_user(
    request: Request,
    registration_service: RegistrationService = Depends(get_registration_service),
    ca_middleware: CredentialAuthenticationMiddleware = Depends(get_credential_authentication_middleware),
    authorization: HTTPAuthorizationCredentials = Depends(security)
):
    if not await ca_middleware.has_access(authorization):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    ip_address = request.client.host
    registration_service.deregister_user(ip_address)

    # TODO: blacklist token

    return {"removed": ip_address}

