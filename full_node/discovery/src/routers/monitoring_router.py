from fastapi import APIRouter, Body, Depends
from models.did import DIDModel
from services.monitoring_service import MonitoringService
from dependencies import get_monitoring_service


monitoring_router = APIRouter(
    dependencies=[Depends(get_monitoring_service)], tags=["monitoring"]
)


@monitoring_router.post("/heartbeat", description="Heartbeat for host monitoring")
async def heartbeat(
    did: DIDModel = Body(..., description="DID of the host"),
    monitoring_service: MonitoringService = Depends(get_monitoring_service),
):
    monitoring_service.heartbeat(did)
    return {"response": "ok"}
