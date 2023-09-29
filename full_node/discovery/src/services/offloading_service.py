from contract import DiscoveryContract
from models.responses import PublishTaskResponse
from services.shared_data_handler import SharedDataHandler
from services.task_publisher import RPCTaskPublisher, BasicTaskPublisher
from models.requests import OffloadRequest
from utils import get_current_timestamp
import uuid
import redis
import models.schema_pb2 as schema


class OffloadingService:
    def __init__(
        self,
        contract: DiscoveryContract,
        rpc_publisher: RPCTaskPublisher,
        basic_publisher: BasicTaskPublisher,
        cache: redis.Redis,
    ) -> None:
        self.contract = contract
        self.rpc_publisher = rpc_publisher
        self.basic_publisher = basic_publisher
        self.cache = cache
        self.shared_data = SharedDataHandler()

    def assign_host_to_client(self, did: str) -> str:
        return self.contract.get_user_queue(get_current_timestamp())

    def remove_host_from_client(self) -> None:
        pass

    async def offload_and_wait(
        self, did: str, offload_request: OffloadRequest
    ) -> PublishTaskResponse:
        queue = self.assign_host_to_client(did)
        if queue == "":
            return {
                "status": 0,
                "response": "",
                "error": "Failed to assign host to client",
            }

        # save correlation_id and origin_did of the message to match the result in result relayer
        correlation_id = str(uuid.uuid4())
        origin_did = offload_request.did
        self.shared_data.save_origin_did(correlation_id, origin_did)

        try:
            response = await self.rpc_publisher.publish(
                correlation_id, offload_request, host_name=queue
            )
            return {"status": 1, "response": response}
        except Exception as e:
            return {"status": 0, "response": correlation_id, "error": str(e)}

    async def offload(
        self, did: str, offload_request: OffloadRequest
    ) -> PublishTaskResponse:
        queue = self.assign_host_to_client(did)
        if queue == "":
            return {
                "status": 0,
                "response": "",
                "error": "Failed to assign host to client",
            }

        # save correlation_id and origin_did of the message to match the result in result relayer
        correlation_id = str(uuid.uuid4())
        origin_did = offload_request.did
        self.shared_data.save_origin_did(correlation_id, origin_did)

        try:
            response = await self.basic_publisher.publish(
                correlation_id, offload_request, host_name=queue
            )
            return {"status": 1, "response": response}
        except Exception as e:
            return {"status": 0, "response": correlation_id, "error": str(e)}

    async def poll_result(self, corr_id_to_find: str) -> schema.TaskResult:
        # look up redis
        result = self.cache.hgetall(corr_id_to_find)
        if len(result) == 0:
            return None

        self.cache.delete(corr_id_to_find)
        return result
