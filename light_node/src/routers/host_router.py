from fastapi import APIRouter, Depends, HTTPException, status
from dependencies import get_config, get_session, get_host_registration_service
from services.host import HostRegistrationService
from config import Config
import aiohttp


host_router = APIRouter(
    prefix="/host",
    tags=["host"],
    dependencies=[
        Depends(get_config),
        Depends(get_session),
        Depends(get_host_registration_service),
    ],
)


@host_router.post("/register_host")
async def register_host(
    credentials: dict,
    session: aiohttp.ClientSession = Depends(get_session),
    config: Config = Depends(get_config),
    host_service: HostRegistrationService = Depends(get_host_registration_service),
):
    async with session.post(
        config.get_register_host_url(), json=credentials
    ) as registration_res:
        if registration_res.status == status.HTTP_200_OK:
            host_service.set_is_registered(True)
            await host_service.start_hosting()

            registration_res_json = await registration_res.json()
            access_token = registration_res_json["access_token"]
            session.headers["Authorization"] = f"Bearer {access_token}"
            return registration_res_json
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to register as host.",
            )


@host_router.get("/deregister_host")
async def register_host(
    session: aiohttp.ClientSession = Depends(get_session),
    config: Config = Depends(get_config),
    host_service: HostRegistrationService = Depends(get_host_registration_service),
):
    if not host_service.is_registered():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not registered as host.",
        )
    async with session.get(config.get_deregister_host_url()) as deregistration_res:
        host_service.set_is_registered(False)
        host_service.stop_hosting()
        return await deregistration_res.json()


# @host_router.post("/get_result")
# async def get_result(
#     req: ComputeResultRequest,
#     host_service: HostRegistrationService = Depends(get_host_registration_service),
# ):
#     result = host_service.get_result(req.id)
#     return {"result": result}
