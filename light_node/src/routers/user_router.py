from fastapi import APIRouter, HTTPException, status, Depends
from config import Config
import aiohttp
from dependencies import (
    get_session,
    get_config,
    get_user_registration_service,
)
from services.user import UserRegistrationService


user_router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[
        Depends(get_config),
        Depends(get_session),
        Depends(get_user_registration_service),
    ],
)


@user_router.post("/register_user")
async def register_user(
    credentials: dict,
    session: aiohttp.ClientSession = Depends(get_session),
    config: Config = Depends(get_config),
    user_service: UserRegistrationService = Depends(get_user_registration_service),
):
    async with session.post(
        config.get_register_user_url(), json=credentials
    ) as registration_res:
        if registration_res.status == status.HTTP_200_OK:
            user_service.set_is_registered(True)
            registration_res_json = await registration_res.json()
            access_token = registration_res_json["access_token"]
            session.headers["Authorization"] = f"Bearer {access_token}"
            return registration_res_json
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to register as user.",
            )


@user_router.get("/deregister_user")
async def register_user(
    session: aiohttp.ClientSession = Depends(get_session),
    config: Config = Depends(get_config),
    user_service: UserRegistrationService = Depends(get_user_registration_service),
):
    if not user_service.is_registered():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not registered as a user.",
        )
    async with session.get(config.get_deregister_user_url()) as deregistration_res:
        user_service.set_is_registered(False)
        return await deregistration_res.json()


@user_router.get("/get_host")
async def get_host(
    session: aiohttp.ClientSession = Depends(get_session),
    config: Config = Depends(get_config),
):
    async with session.get(config.get_assign_host_url()) as res:
        return await res.json()
