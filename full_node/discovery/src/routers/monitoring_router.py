from fastapi import APIRouter, Request, Depends
from services.monitoring_service import MonitoringService
from dependencies import get_monitoring_service


monitoring_router = APIRouter(dependencies=[Depends(get_monitoring_service)])


@monitoring_router.post("/heartbeat")
async def heartbeat(
    request: Request,
    monitoring_service: MonitoringService = Depends(get_monitoring_service),
):
    ip_address = request.client.host
    monitoring_service.heartbeat(ip_address)
    return {"response": "ok"}
