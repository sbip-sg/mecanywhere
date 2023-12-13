from config import Config
import aiohttp

from models.task_result import Resources


class TransactionService:
    def __init__(self, config: Config, session: aiohttp.ClientSession) -> None:
        self.config = config
        self.session = session

    async def record_task(
        self,
        token: str,
        client_did: str,
        client_po_did: str,
        host_did: str,
        host_po_did: str,
        transaction_id: str,
        resource_consumed: Resources,
        transaction_start_datetime: int,
        transaction_end_datetime: int,
        name: str,
        duration: float,
        network_reliability: float,
    ):
        task_metadata = {
            "transaction_id": transaction_id,
            "resource_consumed": resource_consumed.dict(),
            "transaction_start_datetime": int(transaction_start_datetime),
            "transaction_end_datetime": int(transaction_end_datetime),
            "task_name": name,
            "duration": duration,
            "network_reliability": network_reliability,
        }
        request = {
            "client_did": client_did,
            "client_po_did": client_po_did,
            "host_did": host_did,
            "host_po_did": host_po_did,
            "task_metadata": task_metadata,
        }
        return await self.post_transaction(
            token, f"{self.config.get_transaction_service_url()}/record_task", request
        )

    async def update_task(
        self,
        token: str,
        client_did: str,
        client_po_did: str,
        host_did: str,
        host_po_did: str,
        transaction_id: str,
        resource_consumed: Resources,
        transaction_start_datetime: int,
        transaction_end_datetime: int,
        name: str,
        duration: float,
        network_reliability: float,
    ):
        task_metadata = {
            "transaction_id": transaction_id,
            "resource_consumed": resource_consumed.dict(),
            "transaction_start_datetime": int(transaction_start_datetime),
            "transaction_end_datetime": int(transaction_end_datetime),
            "task_name": name,
            "duration": duration,
            "network_reliability": network_reliability,
        }
        request = {
            "client_did": client_did,
            "client_po_did": client_po_did,
            "host_did": host_did,
            "host_po_did": host_po_did,
            "task_metadata": task_metadata,
        }
        return await self.post_transaction(
            token, f"{self.config.get_transaction_service_url()}/update_task", request
        )

    async def post_transaction(self, token: str, url: str, transaction: dict):
        async with self.session.post(
            url,
            json=transaction,
            headers={"Authorization": f"Bearer {token}"},
        ) as resp:
            if resp.status != 200:
                raise ValueError(f"Failed to post transaction: {await resp.text()}")
            return await resp.json()
