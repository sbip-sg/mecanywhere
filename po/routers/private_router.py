from fastapi import APIRouter, Depends, HTTPException, status
from models.account import AccountModel
from models.requests import CreateAccountRequest
from models.responses import UserResponse
from services.account_service import AccountService
from dependencies import get_account_service

private_router = APIRouter(
    dependencies=[Depends(get_account_service)], tags=["private"]
)


@private_router.post(
    "/create_user",
    response_model=UserResponse,
    description="Creates a user as a child of the PO",
)
async def create_user(
    request: CreateAccountRequest,
    account_service: AccountService = Depends(get_account_service),
):
    user_data = account_service.create_user(request)
    return user_data


@private_router.post("/delete_user", response_model=UserResponse)
async def delete_user(
    account: AccountModel,
    account_service: AccountService = Depends(get_account_service),
):
    if not account_service.is_user(account):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user"
        )

    user_data = account_service.delete_user(account)
    return user_data
