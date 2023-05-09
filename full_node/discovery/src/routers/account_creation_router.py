from fastapi import APIRouter, Request, Depends, HTTPException, status
from services.account_creation_service import AccountCreationService
from dependencies import get_account_creation_service

account_creation_router = APIRouter(dependencies=[Depends(get_account_creation_service)])

@account_creation_router.post("/create_account/")
async def create_user(
    request: Request, 
    account_creation_service: AccountCreationService = Depends(get_account_creation_service)
):
    data = await request.json()
    email = data['email']
    password = data['password']
    public_key = data['publicKey']
    public_key_wallet = data['publicKeyWallet']
    user_data = account_creation_service.create_user(email, password, public_key, public_key_wallet)
    return user_data