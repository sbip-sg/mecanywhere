from fastapi import status
from aiohttp import ClientSession
from config import Config
from models.claim import ClaimData


class IssuerService:
    def __init__(self, config: Config, session: ClientSession) -> None:
        self.config = config
        self.session = session

    async def create_vc(self, claim_data: ClaimData):
        claim = {
            "claimData": {**claim_data.dict()},
            "cptId": self.config.get_cpt_id(),
            "issuer": self.config.get_issuer_did(),
        }

        async with self.session.post(
            self.config.get_create_credential_url(), json=claim
        ) as result:
            result_status = result.status
            result_json = await result.json()
            if result_status == status.HTTP_200_OK:
                return result_json