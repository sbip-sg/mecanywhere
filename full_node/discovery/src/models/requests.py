from common.models.credential import CredentialModel
from models.did import DIDModel


class RegistrationRequest(CredentialModel, DIDModel):
    pass


class OffloadRequest(DIDModel):
    container_reference: str
    content: str
