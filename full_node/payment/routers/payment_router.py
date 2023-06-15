from fastapi import APIRouter, Depends
from dependencies import get_did_from_token, get_payment_service
from exceptions.http_exceptions import ForbiddenException
from services.payment_service import PaymentService

payment_router = APIRouter(
    dependencies=[Depends(get_payment_service)], tags=["payment"]
)


@payment_router.post(
    "/stake-notice", description="Submit a notice to stake amount from given address"
)
async def create_stake_notice(
    payment,
    payment_service: PaymentService = Depends(get_payment_service),
    token_did: str = Depends(get_did_from_token),
):
    po_did = payment.did
    payer_addr = payment.payer_address
    amount = payment.amount

    if po_did != token_did:
        raise ForbiddenException("DID does not match token")

    nonce = payment_service.create_payment_notice(po_did, payer_addr, amount)
    return {
        "message": "Please include this reference nonce in the comments of your transaction.",
        "nonce": nonce,
    }


@payment_router.post(
    "/pay-notice", description="Submit a notice to pay tokens from given address"
)
async def create_pay_notice(
    payment,
    payment_service: PaymentService = Depends(get_payment_service),
    token_did: str = Depends(get_did_from_token),
):
    po_did = payment.did
    payer_addr = payment.payer_address
    amount = payment.amount

    if po_did != token_did:
        raise ForbiddenException("DID does not match token")

    nonce = payment_service.create_payment_notice(po_did, payer_addr, amount)
    return {
        "message": "Please include this reference nonce in the comments of your transaction.",
        "nonce": nonce,
    }


@payment_router.post(
    "/receive-wallet-event",
    description="Receive and process wallet transaction from moralis",
)
async def receive_wallet_event(
    event, payment_service: PaymentService = Depends(get_payment_service)
):
    # TODO: Add authentication for event
    transaction = event["txs"][0]
    payer_address = transaction["from_address"]
    amount = transaction["value"]
    nonce = transaction["input"]
    is_confirmed = transaction["confirmed"]

    print(
        f"Transfer received and confirmed {is_confirmed} from {payer_address}: {amount} wei"
    )

    if is_confirmed:
        payment_service.process_payment(payer_address, amount, nonce)


@payment_router.get(
    "/get_balance",
    description="Get balance of given DID that can be used for payment of tasks",
)
async def get_balance(
    did,
    payment_service: PaymentService = Depends(get_payment_service),
    token_did: str = Depends(get_did_from_token),
):
    if did != token_did:
        raise ForbiddenException("DID does not match token")
    return {"balance": payment_service.get_balance(did)}
    # TODO: when to determine if a user has enough balance to pay for a task?
