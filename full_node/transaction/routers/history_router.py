from fastapi import APIRouter, Depends
from dependencies import get_did_from_token, get_history_service
from typing import List
from exceptions.http_exceptions import ForbiddenException
from models.requests import AddDummyHistoryRequest
from models.did import DIDModel
from models.responses import DidRecord, PoDidRecord
from services.history_service import HistoryService

history_router = APIRouter(
    dependencies=[Depends(get_history_service)], tags=["history"]
)


@history_router.post("/find_client_history", response_model=List[DidRecord])
async def find_client_history(
    didModel: DIDModel,
    history_service: HistoryService = Depends(get_history_service),
    token_did: str = Depends(get_did_from_token),
):
    did = didModel.did
    if did != token_did:
        raise ForbiddenException("DID does not match token")

    return history_service.get_did_history(did)


@history_router.post("/find_host_history", response_model=List[DidRecord])
async def find_host_history(
    didModel: DIDModel,
    history_service: HistoryService = Depends(get_history_service),
    token_did: str = Depends(get_did_from_token),
):
    did = didModel.did
    if did != token_did:
        raise ForbiddenException("DID does not match token")

    return history_service.get_did_history(did, host=True)


@history_router.post(
    "/find_po_history",
    response_model=List[PoDidRecord],
    description="Finds all entries that has either given did = client's PO DID or host's PO DID.",
)
async def find_po_history(
    didModel: DIDModel,
    history_service: HistoryService = Depends(get_history_service),
    token_did: str = Depends(get_did_from_token),
):
    did = didModel.did
    if did != token_did:
        raise ForbiddenException("DID does not match token")

    return history_service.get_po_did_history(did)


@history_router.post(
    "/add_dummy_history", description="For testing. All fields optional."
)
async def add_dummy_history(
    request: AddDummyHistoryRequest,
    history_service: HistoryService = Depends(get_history_service),
):
    client_did = request.client_did
    client_po_did = request.client_po_did
    host_did = request.host_did
    host_po_did = request.host_po_did
    if not client_did and not client_po_did and not host_did and not host_po_did:
        return {"message": "No dummy history added"}

    history_service.add_dummy_history(
        client_did=client_did,
        client_po_did=client_po_did,
        host_did=host_did,
        host_po_did=host_po_did,
    )
    return {"message": "Dummy history added"}
