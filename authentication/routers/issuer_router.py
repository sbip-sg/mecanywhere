from fastapi import APIRouter, Depends, HTTPException, status
from services.account_service import AccountService
from services.issuer_service import IssuerService
from models.requests import CreateVcRequest
from models.responses import CreateVcResponse
from dependencies import get_account_service, get_issuer_service

issuer_router = APIRouter(dependencies=[Depends(get_account_service), Depends(get_issuer_service)])

@issuer_router.post("/create_vc/", response_model=CreateVcResponse)
async def create_vc(
    request: CreateVcRequest, 
    issuer_service: IssuerService = Depends(get_issuer_service),
    account_service: AccountService = Depends(get_account_service)
):
    account = request.account
    claim_data = request.claim_data

    if not account_service.verify_user(account):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    
    if not account.did == claim_data.did:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="DID does not match"
        )
        
    credential = await issuer_service.create_vc(claim_data)
    return credential
