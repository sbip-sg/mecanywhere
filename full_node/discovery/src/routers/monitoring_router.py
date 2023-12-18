from fastapi import APIRouter, Depends, Body, status
from exceptions.http_exceptions import ForbiddenException, BadRequestException
from models.did import DIDModel
from services.monitoring_service import MonitoringService
from dependencies import get_monitoring_service, get_did_from_token


monitoring_router = APIRouter(
    dependencies=[Depends(get_monitoring_service)], tags=["monitoring"]
)


@monitoring_router.post(
    "/heartbeat",
    description="Heartbeat for host monitoring. Provide the DID of the host.",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
async def heartbeat(
    didModel: DIDModel = Body(..., description="DID of the host"),
    monitoring_service: MonitoringService = Depends(get_monitoring_service),
    token_did: str = Depends(get_did_from_token)
):
    did = didModel.did
    if did != token_did:
        raise ForbiddenException("DID does not match token")
    if not monitoring_service.is_registered(did):
        raise BadRequestException("Not registered")
    monitoring_service.heartbeat(did)
