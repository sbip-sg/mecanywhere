from contract import DiscoveryContract
from exceptions.http_exceptions import ContractException
from models.user import User
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
        server_host_did: str,
        server_host_po_did: str,
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
        if server_host_name != "":
            self.server_host = User(
                did=server_host_did,
                po_did=server_host_po_did,
                queue=server_host_name,
            )
        self.shared_data = SharedDataHandler()

    def assign_host_to_client(self, did: str) -> User:
        try:
            host = self.contract.get_first_user(get_current_timestamp())
        except Exception as e:
            raise ContractException("Failed to execute contract function: get_first_user: " + str(e))
        if host == None and self.server_host is not None:
            print("Using server-host.")
            return self.server_host
        return host

    def remove_host_from_client(self) -> None:
        pass

    async def offload_and_wait(
        self, did: str, offload_request: OffloadRequest
    ) -> PublishTaskResponse:
        host = self.assign_host_to_client(did)
        if host is None:
            return PublishTaskResponse(
                status=0,
                transaction_id="",
                network_reliability=0,
                error="Failed to assign host to client",
            )
        queue = host.queue

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
                host_did=host.did,
                host_po_did=host.po_did,
                network_reliability=0,
            )
        except Exception as e:
            return PublishTaskResponse(
                status=0,
                transaction_id=correlation_id,
                task_result=None,
                host_did=host.did,
                host_po_did=host.po_did,
                network_reliability=0,
                error=str(e),
            )

    async def offload(
        self, did: str, offload_request: OffloadRequest
    ) -> PublishTaskResponse:
        host = self.assign_host_to_client(did)
        if host is None:
            return PublishTaskResponse(
                status=0,
                transaction_id="",
                network_reliability=0,
                error="Failed to assign host to client",
            )
        queue = host.queue

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
                host_did=host.did,
                host_po_did=host.po_did,
                network_reliability=0,
            )
        except Exception as e:
            return PublishTaskResponse(
                status=0,
                transaction_id=correlation_id,
                task_result=None,
                host_did=host.did,
                host_po_did=host.po_did,
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
