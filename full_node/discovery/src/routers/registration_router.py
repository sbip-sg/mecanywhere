from fastapi import APIRouter, Request, Depends
from services.registration_service import RegistrationService
from dependencies import get_registration_service


registration_router = APIRouter(dependencies=[Depends(get_registration_service)])


@registration_router.get("/register_host")
async def register_host(
    request: Request,
    registration_service: RegistrationService = Depends(get_registration_service),
):
    ip_address = request.client.host
    registration_service.register_host(ip_address)
    return {"response": "ok"}


@registration_router.get("/deregister_host")
async def deregister_host(
    request: Request,
    registration_service: RegistrationService = Depends(get_registration_service),
):
    ip_address = request.client.host
    registration_service.deregister_host(ip_address)
    return {"removed": ip_address}