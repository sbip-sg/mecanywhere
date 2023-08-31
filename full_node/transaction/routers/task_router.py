from fastapi import APIRouter, Depends
from dependencies import get_did_from_token, get_po_did_from_token, get_task_service, get_history_service
from exceptions.http_exceptions import ForbiddenException
from models.requests import RecordTaskRequest
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
    task_type = request.task_type
    did = request.did
    po_did = request.po_did
    task_id = request.task_id
    task_metadata = request.task_metadata
    # TODO: validate task_metadata

    if did != token_did or po_did != token_po_did:
        raise ForbiddenException("DID does not match token")

    price = task_service.process_task(task_type, po_did, task_id, task_metadata)
    history_service.add_did_history(did, task_metadata, price)
    # TODO: handle error and rollback both services
    return price
