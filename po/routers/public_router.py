from fastapi import APIRouter, Depends, HTTPException, status
from services.verifier_service import VerifierService
from services.account_service import AccountService
from services.issuer_service import IssuerService
from models.claim import ClaimSchema
from models.requests import CreateDidRequest, CreateVcRequest
from models.responses import DidServiceResponse
from dependencies import get_account_service, get_issuer_service, get_verifier_service

public_router = APIRouter(
    dependencies=[Depends(get_account_service), Depends(get_issuer_service)],
    tags=["public"],
)


@public_router.post("/user/create_did", response_model=DidServiceResponse)
async def create_did(
    request: CreateDidRequest,
    verifier_service: VerifierService = Depends(get_verifier_service),
):
    public_key = request.public_key
    result = await verifier_service.create_did(public_key)
    return result


@public_router.post("/user/create_vc", response_model=DidServiceResponse)
async def create_vc(
    request: CreateVcRequest,
    issuer_service: IssuerService = Depends(get_issuer_service),
    account_service: AccountService = Depends(get_account_service),
):
    claims = account_service.get_claims(request)
    if claims is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user"
        )

    result = await issuer_service.create_vc(claims)
    return result


@public_router.post("/po/create_schema", response_model=DidServiceResponse)
async def create_schema(
    claim_schema: ClaimSchema,
    issuer_service: IssuerService = Depends(get_issuer_service),
):
    result = await issuer_service.create_schema(claim_schema)
    return result
