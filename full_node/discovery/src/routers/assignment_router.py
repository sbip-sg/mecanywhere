from fastapi import APIRouter, Body, Depends
from models.did import DIDModel
from services.assignment_service import AssignmentService
from dependencies import get_assignment_service


assignment_router = APIRouter(
    dependencies=[Depends(get_assignment_service)], tags=["assignment"]
)


@assignment_router.get(
    "/assign_host", description="Returns host queue for client to join"
)
async def assign_host(
    did: DIDModel = Body(..., description="DID of the client"),
    assignment_service: AssignmentService = Depends(get_assignment_service),
):
    queue = assignment_service.assign(did)
    return {"queue": queue}
