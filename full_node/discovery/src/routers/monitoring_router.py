from fastapi import APIRouter, Body, Depends, status
from models.did import DIDModel
from services.monitoring_service import MonitoringService
from dependencies import get_monitoring_service


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
):
    did = didModel.did
    monitoring_service.heartbeat(did)
