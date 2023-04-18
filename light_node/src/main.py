from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import Config
import aiohttp
from routers.host_router import host_router
from routers.user_router import user_router
from services.host import HostRegistrationService
from services.user import UserRegistrationService


config = Config("../config.json")
session = aiohttp.ClientSession()


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"],
)
app.include_router(host_router)
app.include_router(user_router)


@app.on_event("startup")
async def start_up():
    global host_registration_service
    global user_registration_service
    host_registration_service = HostRegistrationService(config, session)
    user_registration_service = UserRegistrationService()


@app.on_event("shutdown")
async def shut_down():
    if host_registration_service.is_registered():
        host_registration_service.stop_hosting()
        await session.get(config.get_deregister_host_url())
    if user_registration_service.is_registered():
        await session.get(config.get_deregister_user_url())
    await session.close()
