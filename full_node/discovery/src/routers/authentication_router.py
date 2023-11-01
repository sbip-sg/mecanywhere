from fastapi import APIRouter, Depends
from exceptions.http_exceptions import UnauthorizedException
from models.responses import AuthenticationResponse
from models.requests import AuthenticationRequest
from dependencies import get_ca_middleware
from common.middleware.credential_authentication import (
    CredentialAuthenticationMiddleware,
)

authentication_router = APIRouter(
    dependencies=[
        Depends(get_ca_middleware),
    ],
    prefix="/authentication",
    tags=["authentication"],
)


@authentication_router.post("/authenticate", response_model=AuthenticationResponse)
async def register_client(
    request: AuthenticationRequest,
    ca_middleware: CredentialAuthenticationMiddleware = Depends(get_ca_middleware),
):
    credential = request.credential
    did = request.did
    if credential == {}:
        raise UnauthorizedException("No credential provided")
    (access_token, refresh_token) = await ca_middleware.verify_and_create_tokens(
        did, credential
    )
    return {
        "access_token": access_token,
        "access_token_type": "Bearer",
        "refresh_token": refresh_token,
        "refresh_token_type": "Bearer",
    }


@authentication_router.post("/refresh_access")
async def refresh_access(
    refresh_token: str,
    ca_middleware: CredentialAuthenticationMiddleware = Depends(get_ca_middleware),
):
    access_token = await ca_middleware.refresh_access(refresh_token)
    return {"access_token": access_token, "access_token_type": "Bearer"}
