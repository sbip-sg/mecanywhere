from fastapi import APIRouter, Request, Depends
from services.account_service import AccountService
from dependencies import get_account_service

account_router = APIRouter(dependencies=[Depends(get_account_service)])

@account_router.post("/create_account/")
async def create_account(
    request: Request, 
    account_service: AccountService = Depends(get_account_service)
):
    data = await request.json()
    email = data['email']
    password = data['password']
    print("email", email)
    print("password", password)
    user_data = account_service.create_user(email, password)
    return user_data