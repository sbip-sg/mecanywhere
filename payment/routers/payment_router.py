from fastapi import APIRouter, Depends, HTTPException
from contract import PaymentContract
from dependencies import get_contract_instance, get_did_from_token
from exceptions.http_exceptions import ForbiddenException
from models.requests import WithdrawalRequest

payment_router = APIRouter(tags=["payment"])


@payment_router.post("/withdraw", description="For POs to withdraw from their balance.")
async def withdraw(
    withdrawal: WithdrawalRequest,
    contract: PaymentContract = Depends(get_contract_instance),
    token_did: str = Depends(get_did_from_token),
):
    did = withdrawal.did
    address = withdrawal.address
    amount = withdrawal.amount

    if did != token_did:
        raise ForbiddenException("DID does not match token")

    try:
        contract.withdraw(did, address, amount)
        balance = contract.get_balance(did)
        return {"message": "Withdrawal successful.", "balance": balance}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
