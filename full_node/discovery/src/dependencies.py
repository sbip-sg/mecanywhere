from middleware.credential_authentication import CredentialAuthenticationMiddleware
import main
from services.assignment_service import AssignmentService
from services.registration_service import RegistrationService
from services.monitoring_service import MonitoringService
from services.account_creation_service import AccountCreationService
from services.login_service import LoginService

def get_credential_authentication_middleware() -> CredentialAuthenticationMiddleware:
    return main.ca_middleware

def get_account_creation_service() -> AccountCreationService:
    return main.account_creation_service

def get_login_service() -> LoginService:
    return main.login_service

def get_assignment_service() -> AssignmentService:
    return main.assignment_service

def get_registration_service() -> RegistrationService:
    return main.registration_service

def get_monitoring_service() -> MonitoringService:
    return main.monitoring_service