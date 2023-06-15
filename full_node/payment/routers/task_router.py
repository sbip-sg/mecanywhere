from fastapi import APIRouter, Depends
from dependencies import get_did_from_token, get_po_did_from_token, get_task_service
from exceptions.http_exceptions import ForbiddenException
from services.task_service import TaskService

task_router = APIRouter(dependencies=[Depends(get_task_service)], tags=["task"])


@task_router.post(
    "/record_task",
    description="For clients or hosts to record a task's offload or completion. "
    + "This calculates the fee and updates the balance of the host and client.",
)
async def record_task(
    task,
    task_service: TaskService = Depends(get_task_service),
    token_did: str = Depends(get_did_from_token),
    token_po_did: str = Depends(get_po_did_from_token),
):
    task_type = task.task_type
    did = task.did
    po_did = task.po_did
    task_id = task.task_id
    task_metadata = task.task_metadata

    if did != token_did or po_did != token_po_did:
        raise ForbiddenException("DID does not match token")

    task_service.process_task(task_type, po_did, task_id, task_metadata)
