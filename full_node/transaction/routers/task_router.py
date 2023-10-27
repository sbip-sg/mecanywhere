from fastapi import APIRouter, Depends
from dependencies import (
    get_did_from_token,
    get_po_did_from_token,
    get_task_service,
    get_history_service,
)
from exceptions.http_exceptions import ForbiddenException, BadRequestException
from models.requests import RecordTaskRequest, UpdateTaskRequest
from services.history_service import HistoryService
from services.task_service import TaskService

task_router = APIRouter(dependencies=[Depends(get_task_service)], tags=["task"])


@task_router.post(
    "/record_task",
    description="For users to record a task's offload or completion. "
    + "This calculates the fee and updates the balance of the host and client.",
)
async def record_task(
    request: RecordTaskRequest,
    task_service: TaskService = Depends(get_task_service),
    history_service: HistoryService = Depends(get_history_service),
    token_did: str = Depends(get_did_from_token),
    token_po_did: str = Depends(get_po_did_from_token),
):
    client_did = request.client_did
    client_po_did = request.client_po_did
    host_po_did = request.host_po_did
    task_metadata = request.task_metadata
    # TODO: validate task_metadata

    if client_did != token_did or client_po_did != token_po_did:
        raise ForbiddenException("DID does not match token")

    price = task_service.process_task(client_po_did, host_po_did, task_metadata)
    history_service.add_did_history(request, price)
    # TODO: handle error and rollback both services
    return price


@task_router.post(
    "/update_task",
    description="For users to update a task's offload or completion. "
    + "This calculates the fee and updates the balance of the host and client.",
)
async def update_task(
    request: UpdateTaskRequest,
    task_service: TaskService = Depends(get_task_service),
    history_service: HistoryService = Depends(get_history_service),
    token_did: str = Depends(get_did_from_token),
    token_po_did: str = Depends(get_po_did_from_token),
):
    client_did = request.client_did
    client_po_did = request.client_po_did
    task_metadata = request.task_metadata

    if client_did != token_did or client_po_did != token_po_did:
        raise ForbiddenException("DID does not match token")

    transaction = history_service.get_transaction(client_did, task_metadata.transaction_id)
    if transaction is None:
        raise BadRequestException("Task does not exist")
    host_po_did = transaction.host_po_did

    price = task_service.process_task(client_po_did, host_po_did, task_metadata)
    history_service.update_did_history(request, price)

    return price
