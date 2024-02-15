import asyncio
import json
from exceptions.http_exceptions import ContractException
from contracts.scheduler_contract import SchedulerContract
from services.cache import DCache
from models.scheduler import Task
from models.task_result import Resources
from models.responses import PublishTaskResponse, TaskResultModel
from services.message_queue.task_publisher import BasicTaskPublisher
from models.requests import OffloadRequest
import uuid

MAX_TIMEOUT = 60 * 10


class  OffloadingService:
    def __init__(
        self,
        contract: SchedulerContract,
        publisher: BasicTaskPublisher,
        cache: DCache,
    ) -> None:
        self.contract = contract
        self.publisher = publisher
        self.cache = cache
        if not self.cache.ping():
            raise Exception("Cache is not running")

    async def offload_and_wait(
        self, did: str, host_addr: str, offload_request: OffloadRequest
    ) -> PublishTaskResponse:
        publish_receipt = await self.offload(did, host_addr, offload_request)
        if publish_receipt.status == 0:
            return publish_receipt
        transaction_id = publish_receipt.transaction_id
        host_did = publish_receipt.host_did

        response = None
        clock = 0
        while response is None:
            if clock > MAX_TIMEOUT:
                return PublishTaskResponse(
                    status=0,
                    transaction_id=transaction_id,
                    task_result=None,
                    host_did=host_did,
                    network_reliability=0,
                    error="Time out.",
                )
            await asyncio.sleep(0.1)
            response = await self.poll_result(transaction_id)
            clock += 0.1
        response.host_did = host_did
        return response

    async def offload(
        self, host_addr: str, offload_request: OffloadRequest
    ) -> PublishTaskResponse:
        resources = offload_request.resource
        if resources is None:
            resources = Resources()

        queue = host_addr
        transaction_id = str(uuid.uuid4())

        try:
            receipt = await self.publisher.publish(
                transaction_id,
                offload_request,
                host_name=queue,
            )
        except Exception as e:
            return PublishTaskResponse(
                status=0,
                transaction_id=transaction_id,
                task_result=None,
                host_did=host_addr,
                network_reliability=0,
                error=str(e),
            )
        return PublishTaskResponse(
            status=1,
            transaction_id=transaction_id,
            task_result=receipt,
            host_did=host_addr,
            network_reliability=0,
            error="",
        )

    async def poll_result(self, corr_id_to_find: str) -> PublishTaskResponse:
        result = self.cache.get_result(corr_id_to_find)
        if result is None:
            return None

        self.cache.delete_result(corr_id_to_find)
        task_result_model = TaskResultModel(**json.loads(result))
        publish_task_response = PublishTaskResponse(
            status=1,
            transaction_id=corr_id_to_find,
            task_result=task_result_model,
            network_reliability=0,
        )
        return publish_task_response

    async def get_task_record(self, task_hash: str) -> Task:
        try:
            return self.contract.get_running_task(task_hash)
        except Exception as e:
            raise ContractException(
                "Failed to execute contract function: get_running_task: " + str(e)
            )
