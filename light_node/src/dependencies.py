import main
from services.host import HostRegistrationService
from services.user import UserRegistrationService
from config import Config
import aiohttp


def get_host_registration_service() -> HostRegistrationService:
    return main.host_registration_service


def get_user_registration_service() -> UserRegistrationService:
    return main.user_registration_service


def get_session() -> aiohttp.ClientSession:
    return main.session


def get_config() -> Config:
    return main.config
