from fastapi import APIRouter, Request, Depends
from services.registration_service import RegistrationService
from dependencies import get_registration_service
from middleware.credential_authentication import CredentialAuthenticationMiddleware

registration_router = APIRouter(
    dependencies=[Depends(get_registration_service)], prefix="/registration"
)

create_access_token = CredentialAuthenticationMiddleware.create_access_token


@registration_router.get("/register_host")
async def register_host(
    request: Request,
    registration_service: RegistrationService = Depends(get_registration_service),
):
    ip_address = request.client.host
    registration_service.register_host(ip_address)
    access_token = create_access_token(data={"sub": "test"})
    return {"response": "ok", "access_token": access_token, "token_type": "bearer"}


@registration_router.get("/deregister_host")
async def deregister_host(
    request: Request,
    registration_service: RegistrationService = Depends(get_registration_service),
):
    ip_address = request.client.host
    registration_service.deregister_host(ip_address)

    # TODO: blacklist token

    return {"removed": ip_address}
