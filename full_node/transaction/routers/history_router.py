from fastapi import APIRouter, Depends
from dependencies import get_did_from_token, get_history_service, get_po_did_from_token
from typing import List
from exceptions.http_exceptions import ForbiddenException
from models.did import DIDModel
from models.responses import DidRecord, PoDidRecord
from services.history_service import HistoryService

history_router = APIRouter(
    dependencies=[Depends(get_history_service)], tags=["history"]
)


@history_router.post("/find_did_history", response_model=List[DidRecord])
async def find_did_history(
    didModel: DIDModel,
    history_service: HistoryService = Depends(get_history_service),
    token_did: str = Depends(get_did_from_token),
):
    did = didModel.did
    if did != token_did:
        raise ForbiddenException("DID does not match token")

    return history_service.get_did_history(did)


@history_router.post("/find_po_history", response_model=List[PoDidRecord])
async def find_po_history(
    didModel: DIDModel,
    history_service: HistoryService = Depends(get_history_service),
    token_did: str = Depends(get_did_from_token),
):
    did = didModel.did
    if did != token_did:
        raise ForbiddenException("DID does not match token")

    return history_service.get_po_did_history(did)


@history_router.post("/add_dummy_history")
async def add_dummy_history(
    didModel: DIDModel,
    history_service: HistoryService = Depends(get_history_service),
    token_did: str = Depends(get_did_from_token),
    po_did: str = Depends(get_po_did_from_token),
):
    did = didModel.did

    if did != token_did:
        raise ForbiddenException("DID does not match token")

    history_service.add_dummy_history(did, po_did)
    return {"message": "Dummy history added"}
