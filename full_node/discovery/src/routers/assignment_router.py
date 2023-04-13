from fastapi import APIRouter, Depends
from services.assignment_service import AssignmentService
from dependencies import get_assignment_service


assignment_router = APIRouter(dependencies=[Depends(get_assignment_service)])


@assignment_router.get("/assign_host")
async def assign_host(
    assignment_service: AssignmentService = Depends(get_assignment_service),
):
    ip_address = assignment_service.assign()
    return {"ip_address": ip_address}
