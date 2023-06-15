from fastapi import APIRouter, Body, Depends
from exceptions.http_exceptions import ForbiddenException
from models.responses import AssignmentResponse
from models.did import DIDModel
from services.assignment_service import AssignmentService
from dependencies import get_assignment_service, get_did_from_token


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
    token_did: str = Depends(get_did_from_token),
):
    did = didModel.did
    if did != token_did:
        raise ForbiddenException("DID does not match token")
    queue = assignment_service.assign(did)
    return {"queue": queue}
