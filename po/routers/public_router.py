from fastapi import APIRouter, Depends
from exceptions.http_exceptions import BadRequestException
from services.verifier_service import VerifierService
from services.account_service import AccountService
from services.issuer_service import IssuerService
from models.claim import ClaimSchema
from models.requests import CreateUserRequest
from models.responses import CreateUserResponse, DidServiceResponse
from dependencies import get_account_service, get_issuer_service, get_verifier_service

public_router = APIRouter(
    dependencies=[Depends(get_account_service), Depends(get_issuer_service)],
    tags=["public"],
)


@public_router.post(
    "/user/create_user",
    response_model=CreateUserResponse,
    description="Creates a user from a created customer account, "
    "and creates a DID and credential for the user using the public key provided. "
    "Overwrites previous DID if one already exists."
    "The claims for the credential are retrieved from the customer account.",
)
async def create_did(
    request: CreateUserRequest,
    verifier_service: VerifierService = Depends(get_verifier_service),
    account_service: AccountService = Depends(get_account_service),
    issuer_service: IssuerService = Depends(get_issuer_service),
):
    public_key = request.public_key
    account = request.account
    user = account_service.get_user(account)
    if user is None:
        raise BadRequestException("Error: Customer does not exist.")

    did = user.did
    prev_pubkey = user.pubkey
    # create DID if user does not have one or if the public key has changed
    if did is None or prev_pubkey != public_key:
        did_result = await verifier_service.create_did(public_key)
        did_response = DidServiceResponse(**did_result)
        if did_response.errorCode != 0:
            raise BadRequestException(
                f"Error: Failed to create DID. {did_response.errorMessage}"
            )

        did = did_response.result["did"]
        account_service.update_did_and_pubkey(account, did, public_key)

    claims = account_service.get_claims(account)
    vc_result = await issuer_service.create_vc(claims)
    vc_response = DidServiceResponse(**vc_result)
    if vc_response.errorCode != 0:
        raise BadRequestException(
            f"Error: Failed to create VC. {vc_response.errorMessage}"
        )

    return {
        "did": did,
        "credential": vc_response.result,
    }


@public_router.post("/po/create_schema", response_model=DidServiceResponse)
async def create_schema(
    claim_schema: ClaimSchema,
    issuer_service: IssuerService = Depends(get_issuer_service),
):
    result = await issuer_service.create_schema(claim_schema)
    return result
