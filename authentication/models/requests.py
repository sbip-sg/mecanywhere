from pydantic import BaseModel
from models.account import AccountModel
from models.claim import ClaimData

class CreateVcRequest(BaseModel):
    claim_data: ClaimData
    account: AccountModel
