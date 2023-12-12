from fastapi import APIRouter, Depends
from exceptions.http_exceptions import ForbiddenException
from models.responses import OffloadResponse, PublishTaskResponse
from models.requests import OffloadRequest, PollResultRequest
from services.offloading_service import OffloadingService
from services.transaction_service import TransactionService
from dependencies import (
    get_offloading_service,
    get_did_from_token,
    get_transaction_service,
    get_token,
    get_po_did_from_token,
)


offload_router = APIRouter(
    dependencies=[Depends(get_offloading_service)],
    tags=["offloading"],
    prefix="/offloading",
)


@offload_router.post("/offload_task_and_get_result", response_model=OffloadResponse)
async def offload_task_and_get_result(
    offload_request: OffloadRequest,
    offloading_service: OffloadingService = Depends(get_offloading_service),
    transaction_service: TransactionService = Depends(get_transaction_service),
    token: str = Depends(get_token),
    token_did: str = Depends(get_did_from_token),
    po_did: str = Depends(get_po_did_from_token),
):
    did = offload_request.did
    if did != token_did:
        raise ForbiddenException("DID does not match token")
    task_id = offload_request.task_id
    response = await offloading_service.offload_and_wait(did, offload_request)
    if response.status == 1:
        return await record_response(transaction_service, token, did, po_did, response)
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
    transaction_service: TransactionService = Depends(get_transaction_service),
    token: str = Depends(get_token),
    token_did: str = Depends(get_did_from_token),
    po_did: str = Depends(get_po_did_from_token),
):
    did = offload_request.did
    task_id = offload_request.task_id
    if did != token_did:
        raise ForbiddenException("DID does not match token")
    response = await offloading_service.offload(did, offload_request)
    if response.status == 1:
        return await record_response(transaction_service, token, did, po_did, response)
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
    transaction_service: TransactionService = Depends(get_transaction_service),
    token: str = Depends(get_token),
    token_did: str = Depends(get_did_from_token),
    po_did: str = Depends(get_po_did_from_token),
):
    did = poll_result_request.did
    transaction_id = poll_result_request.transaction_id
    if did != token_did:
        raise ForbiddenException("DID does not match token")
    response = await offloading_service.poll_result(transaction_id)
    if response is None:
        return OffloadResponse(
            transaction_id=transaction_id,
            task_id=transaction_id,
            status=0,
            response="",
            error="No result found",
        )
    return await record_response(
        transaction_service, token, did, po_did, response, is_update=True
    )


async def record_response(
    transaction_service: TransactionService,
    token: str,
    client_did: str,
    client_po_did: str,
    response: PublishTaskResponse,
    is_update: bool = False,
):
    task_result = response.task_result
    offload_response = OffloadResponse(
        transaction_id=response.transaction_id,
        task_id=task_result.id,
        status=response.status,
        response=task_result.content,
    )
    host_did = response.host_did
    host_po_did = response.host_po_did
    try:
        print("recording task in transaction service")
        record_func = (
            transaction_service.update_task
            if is_update
            else transaction_service.record_task
        )
        await record_func(
            token,
            client_did,
            client_po_did,
            host_did,
            host_po_did,
            response.transaction_id,
            task_result.resource_consumed,
            task_result.transaction_start_datetime,
            task_result.transaction_end_datetime,
            task_result.id,
            task_result.duration,
            response.network_reliability,
        )
    except Exception as e:
        offload_response.error = "Error recording task: " + str(e)
    return offload_response
