from fastapi import APIRouter, Body, Depends, status
from exceptions.http_exceptions import ForbiddenException
from models.did import DIDModel
from services.monitoring_service import MonitoringService
from dependencies import get_monitoring_service, get_did_from_token, get_po_did_from_token


monitoring_router = APIRouter(
    dependencies=[Depends(get_monitoring_service)], tags=["monitoring"]
)


@monitoring_router.post(
    "/heartbeat",
    description="Heartbeat for host monitoring",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
async def heartbeat(
    didModel: DIDModel = Body(..., description="DID of the host"),
    monitoring_service: MonitoringService = Depends(get_monitoring_service),
    token_did: str = Depends(get_did_from_token),
    token_po_did: str = Depends(get_po_did_from_token),
):
    did = didModel.did
    if did != token_did:
        raise ForbiddenException("DID does not match token")
    monitoring_service.heartbeat(did, token_po_did)
