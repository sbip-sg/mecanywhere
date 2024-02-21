from fastapi import APIRouter, Depends
from models.responses import OffloadResponse
from models.requests import OffloadRequest, PollResultRequest
from services.offloading_service import OffloadingService
from dependencies import get_offloading_service


offload_router = APIRouter(
    dependencies=[Depends(get_offloading_service)],
    tags=["offloading"],
    prefix="/offloading",
)


@offload_router.post("/offload_task_and_get_result", response_model=OffloadResponse)
async def offload_task_and_get_result(
    offload_request: OffloadRequest,
    offloading_service: OffloadingService = Depends(get_offloading_service),
):
    did = offload_request.did
    task = await offloading_service.get_task_record(did, offload_request)
    host = task.host_address
    task_id = offload_request.task_id
    response = await offloading_service.offload_and_wait(did, host, offload_request)
    if response.status == 1:
        task_result = response.task_result
        return OffloadResponse(
            transaction_id=response.transaction_id,
            task_id=task_result.id,
            status=response.status,
            response=task_result.content,
        )
    else:
        return OffloadResponse(
            transaction_id=response.transaction_id,
            task_id=task_id,
            status=response.status,
            response="",
            error=response.error,
        )


@offload_router.post("/offload_task", response_model=OffloadResponse)
async def offload_task(
    offload_request: OffloadRequest,
    offloading_service: OffloadingService = Depends(get_offloading_service),
):
    did = offload_request.did
    task_id = offload_request.task_id
    task = await offloading_service.get_task_record(did, offload_request)
    host = task.host_address
    response = await offloading_service.offload(did, host, offload_request)
    if response.status == 1:
        task_result = response.task_result
        return OffloadResponse(
            transaction_id=response.transaction_id,
            task_id=task_result.id,
            status=response.status,
            response=task_result.content,
        )
    else:
        return OffloadResponse(
            transaction_id=response.transaction_id,
            task_id=task_id,
            status=response.status,
            response="",
            error=response.error,
        )


@offload_router.post("/poll_result", response_model=OffloadResponse)
async def poll_result(
    poll_result_request: PollResultRequest,
    offloading_service: OffloadingService = Depends(get_offloading_service),
):
    transaction_id = poll_result_request.transaction_id
    response = await offloading_service.poll_result(transaction_id)
    if response is None:
        return OffloadResponse(
            transaction_id=transaction_id,
            task_id=transaction_id,
            status=0,
            response="",
            error="No result found",
        )
    task_result = response.task_result
    return OffloadResponse(
        transaction_id=response.transaction_id,
        task_id=task_result.id,
        status=response.status,
        response=task_result.content,
    )
