from fastapi import APIRouter, Request, Depends
from models.account import AccountModel
from models.responses import CreateUserResponse
from services.account_service import AccountService
from dependencies import get_account_service

account_router = APIRouter(dependencies=[Depends(get_account_service)])

@account_router.post("/create_user/", response_model=CreateUserResponse)
async def create_user(
    account: AccountModel,
    account_service: AccountService = Depends(get_account_service)
):
    user_data = account_service.create_user(account)
    return user_data