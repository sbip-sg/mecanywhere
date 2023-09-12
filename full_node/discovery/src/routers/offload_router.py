from fastapi import APIRouter, Body, Depends
from exceptions.http_exceptions import ForbiddenException
from models.requests import OffloadRequest
from services.offloading_service import OffloadingService
from dependencies import get_offloading_service, get_did_from_token


offload_router = APIRouter(
    dependencies=[Depends(get_offloading_service)], tags=["offloading"]
)


@offload_router.post(
    "/offload_to_host",
)
async def offload_to_host(
    offload_request: OffloadRequest,
    offloading_service: OffloadingService = Depends(get_offloading_service),
    token_did: str = Depends(get_did_from_token),
):
    did = offload_request.did
    if did != token_did:
        raise ForbiddenException("DID does not match token")
    status = offloading_service.offload_to_queue(did, offload_request)
    return {"status": status}
