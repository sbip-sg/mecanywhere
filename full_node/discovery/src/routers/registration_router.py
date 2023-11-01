from fastapi import APIRouter, Depends, status
from exceptions.http_exceptions import ForbiddenException, BadRequestException, ContractException
from models.did import DIDModel
from services.registration_service import RegistrationService
from dependencies import (
    get_registration_service,
    get_ca_middleware,
    get_did_from_token,
    get_po_did_from_token,
)

registration_router = APIRouter(
    dependencies=[
        Depends(get_registration_service),
        Depends(get_ca_middleware),
    ],
    prefix="/registration",
    tags=["registration"],
)


@registration_router.post(
    "/register_host", response_model=None
)
async def register_host(
    didModel: DIDModel,
    registration_service: RegistrationService = Depends(get_registration_service),
    token_did: str = Depends(get_did_from_token),
    token_po_did: str = Depends(get_po_did_from_token),
):
    did = didModel.did
    if did != token_did:
        raise ForbiddenException("DID does not match token")
    try:
        registration_service.register_host(did, token_po_did)
    except Exception as e:
        print(e)
        raise ContractException(str(e))


@registration_router.post(
    "/deregister_host",
    response_model=None,
)
async def deregister_host(
    didModel: DIDModel,
    registration_service: RegistrationService = Depends(get_registration_service),
    token_did: str = Depends(get_did_from_token),
):
    did = didModel.did
    if did != token_did:
        raise ForbiddenException("DID does not match token")
    try:
        if not registration_service.is_registered(did):
            raise BadRequestException("Host is not registered")
        registration_service.deregister_host(did)
    except Exception as e:
        print(e)
        raise ContractException(str(e))
    # TODO: blacklist token


@registration_router.post(
    "/register_client", response_model=None
)
async def register_client(
    didModel: DIDModel,
    registration_service: RegistrationService = Depends(get_registration_service),
    token_did: str = Depends(get_did_from_token),
):
    did = didModel.did
    if did != token_did:
        raise ForbiddenException("DID does not match token")
    try:
        registration_service.register_client(did)
    except Exception as e:
        print(e)
        raise ContractException(str(e))


@registration_router.post(
    "/deregister_client",
    response_model=None,
)
async def deregister_client(
    didModel: DIDModel,
    registration_service: RegistrationService = Depends(get_registration_service),
    token_did: str = Depends(get_did_from_token),
):
    did = didModel.did
    if did != token_did:
        raise ForbiddenException("DID does not match token")
    try:
        registration_service.deregister_client(did)
    except Exception as e:
        print(e)
        raise ContractException(str(e))
    # TODO: blacklist token
