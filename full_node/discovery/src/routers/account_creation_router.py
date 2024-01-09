from fastapi import APIRouter, Request, Depends, HTTPException, status
from services.account_creation_service import AccountCreationService
from dependencies import get_account_creation_service

account_creation_router = APIRouter(dependencies=[Depends(get_account_creation_service)])

@account_creation_router.post("/create_account/", deprecated=True)
async def create_user(
    request: Request, 
    account_creation_service: AccountCreationService = Depends(get_account_creation_service)
):
    data = await request.json()
    public_key = data['publicKey']
    user_data = account_creation_service.create_user(public_key)
    return user_data