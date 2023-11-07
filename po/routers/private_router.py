from fastapi import APIRouter, Depends
from models.db_schema import AccountModel
from models.requests import CreateAccountRequest
from models.responses import UserResponse
from exceptions.http_exceptions import BadRequestException
from services.account_service import AccountService
from dependencies import get_account_service

private_router = APIRouter(
    dependencies=[Depends(get_account_service)], tags=["private"]
)


@private_router.post(
    "/create_customer",
    response_model=UserResponse,
    description="Creates a user as a child of the PO",
)
async def create_customer(
    request: CreateAccountRequest,
    account_service: AccountService = Depends(get_account_service),
):
    user_data = account_service.create_user(request)
    return user_data


@private_router.post("/delete_customer", response_model=UserResponse)
async def delete_customer(
    account: AccountModel,
    account_service: AccountService = Depends(get_account_service),
):
    if not account_service.is_user(account):
        raise BadRequestException("Invalid Customer")

    user_data = account_service.delete_user(account)
    return user_data
