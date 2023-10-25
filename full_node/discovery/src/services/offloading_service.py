from contract import DiscoveryContract
from models.responses import PublishTaskResponse, TaskResultModel
from services.message_queue.shared_data_handler import SharedDataHandler
from services.message_queue.task_publisher import RPCTaskPublisher, BasicTaskPublisher
from models.requests import OffloadRequest
from utils import get_current_timestamp
import uuid
import redis


class OffloadingService:
    def __init__(
        self,
        contract: DiscoveryContract,
        rpc_publisher: RPCTaskPublisher,
        basic_publisher: BasicTaskPublisher,
        cache: redis.Redis,
        server_host_name: str,
    ) -> None:
        self.contract = contract
        self.rpc_publisher = rpc_publisher
        self.basic_publisher = basic_publisher
        self.cache = cache
        try:
            self.cache.ping()
        except redis.exceptions.ConnectionError as e:
            print("Redis connection error: ", e)
            self.cache = None
        self.server_host_name = server_host_name
        self.shared_data = SharedDataHandler()

    def assign_host_to_client(self, did: str) -> str:
        host = self.contract.get_user_queue(get_current_timestamp())
        if host == "" and self.server_host_name is not None:
            print("Using server-host.")
            host = self.server_host_name
        return host

    def remove_host_from_client(self) -> None:
        pass

    async def offload_and_wait(
        self, did: str, offload_request: OffloadRequest
    ) -> PublishTaskResponse:
        queue = self.assign_host_to_client(did)
        if queue == "":
            return PublishTaskResponse(
                status=0,
                transaction_id="",
                task_result=None,
                network_reliability=0,
                error="Failed to assign host to client",
            )

        # save correlation_id and origin_did of the message to match the result in result relayer
        correlation_id = str(uuid.uuid4())
        origin_did = offload_request.did
        self.shared_data.save_origin_did(correlation_id, origin_did)

        try:
            response = await self.rpc_publisher.publish(
                correlation_id, offload_request, host_name=queue
            )
            return PublishTaskResponse(
                status=1,
                transaction_id=correlation_id,
                task_result=response,
                network_reliability=0,
            )
        except Exception as e:
            return PublishTaskResponse(
                status=0,
                transaction_id=correlation_id,
                task_result=None,
                network_reliability=0,
                error=str(e),
            )

    async def offload(
        self, did: str, offload_request: OffloadRequest
    ) -> PublishTaskResponse:
        queue = self.assign_host_to_client(did)
        if queue == "":
            return PublishTaskResponse(
                status=0,
                transaction_id="",
                task_result=None,
                network_reliability=0,
                error="Failed to assign host to client",
            )

        # save correlation_id and origin_did of the message to match the result in result relayer
        correlation_id = str(uuid.uuid4())
        origin_did = offload_request.did
        self.shared_data.save_origin_did(correlation_id, origin_did)

        try:
            response = await self.basic_publisher.publish(
                correlation_id, offload_request, host_name=queue
            )
            return PublishTaskResponse(
                status=1,
                transaction_id=correlation_id,
                task_result=response,
                network_reliability=0,
            )
        except Exception as e:
            return PublishTaskResponse(
                status=0,
                transaction_id=correlation_id,
                task_result=None,
                network_reliability=0,
                error=str(e),
            )

    async def poll_result(self, corr_id_to_find: str) -> PublishTaskResponse:
        # look up redis
        if self.cache is None:
            print("Redis is not connected.")
            return None
        result = self.cache.hgetall(corr_id_to_find)
        if len(result) == 0:
            return None

        self.cache.delete(corr_id_to_find)
        task_result_model = TaskResultModel(**result)
        publish_task_response = PublishTaskResponse(
            status=1,
            transaction_id=corr_id_to_find,
            task_result=task_result_model,
            network_reliability=0,
        )
        return publish_task_response
