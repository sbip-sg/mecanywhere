from fastapi import APIRouter, Depends
from exceptions.http_exceptions import ForbiddenException
from models.responses import OffloadResponse
from models.requests import OffloadRequest, PollResultRequest
from services.offloading_service import OffloadingService
from dependencies import get_offloading_service, get_did_from_token


offload_router = APIRouter(
    dependencies=[Depends(get_offloading_service)],
    tags=["offloading"],
    prefix="/offloading",
)


@offload_router.post("/offload_task_and_get_result", response_model=OffloadResponse)
async def offload_task_and_get_result(
    offload_request: OffloadRequest,
    offloading_service: OffloadingService = Depends(get_offloading_service),
    token_did: str = Depends(get_did_from_token),
):
    did = offload_request.did
    task_id = offload_request.task_id
    if did != token_did:
        raise ForbiddenException("DID does not match token")
    result = await offloading_service.offload_and_wait(did, offload_request)
    # record task
    return result | {"task_id": task_id}


@offload_router.post("/offload_task", response_model=OffloadResponse)
async def offload_task(
    offload_request: OffloadRequest,
    offloading_service: OffloadingService = Depends(get_offloading_service),
    token_did: str = Depends(get_did_from_token),
):
    did = offload_request.did
    task_id = offload_request.task_id
    if did != token_did:
        raise ForbiddenException("DID does not match token")
    result = await offloading_service.offload(did, offload_request)
    # record task
    return result | {"task_id": task_id}


@offload_router.post("/poll_result", response_model=OffloadResponse)
async def poll_result(
    poll_result_request: PollResultRequest,
    offloading_service: OffloadingService = Depends(get_offloading_service),
    token_did: str = Depends(get_did_from_token),
):
    did = poll_result_request.did
    correlation_id = poll_result_request.correlation_id
    if did != token_did:
        raise ForbiddenException("DID does not match token")
    result = await offloading_service.poll_result(correlation_id)
    # record task
    if result is None:
        return {
            "task_id": "",
            "status": 0,
            "response": correlation_id,
            "error": "No result",
        }
    return {"task_id": result.get("id"), "status": 1, "response": result.get("content")}
