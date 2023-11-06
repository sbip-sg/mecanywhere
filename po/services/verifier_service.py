from fastapi import HTTPException, status
from aiohttp import ClientSession
from config import Config


class VerifierService:
    def __init__(self, config: Config, session: ClientSession) -> None:
        self.config = config
        self.session = session

    async def create_did(self, public_key: str):
        request_payload = {"publicKey": public_key}
        return await self._post_request(
            self.config.get_verifier_url() + "/api/v1/did/create", request_payload
        )

    async def _post_request(self, url, payload):
        print("POST", url, payload)
        async with self.session.post(url, json=payload) as result:
            result_status = result.status
            result_json = await result.json()
            if result_status == status.HTTP_200_OK:
                return result_json
            raise HTTPException(
                status_code=result_status,
                detail=result_json["error"],
            )
