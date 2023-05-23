from fastapi import APIRouter, Body, Depends
from models.responses import AssignmentResponse
from models.did import DIDModel
from services.assignment_service import AssignmentService
from dependencies import get_assignment_service


assignment_router = APIRouter(
    dependencies=[Depends(get_assignment_service)], tags=["assignment"]
)


@assignment_router.post(
    "/assign_host",
    description="Returns host queue for client to join",
    response_model=AssignmentResponse,
)
async def assign_host(
    didModel: DIDModel = Body(..., description="DID of the client"),
    assignment_service: AssignmentService = Depends(get_assignment_service),
):
    print("didModel", didModel)
    did = didModel.did
    queue = assignment_service.assign(did)
    return {"queue": queue}
