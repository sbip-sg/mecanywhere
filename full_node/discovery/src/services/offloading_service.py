from contract import DiscoveryContract
from services.shared_data_handler import SharedDataHandler
from services.task_publisher import TaskPublisher
from models.requests import OffloadRequest
from utils import get_current_timestamp
import uuid


class OffloadingService:
    def __init__(self, contract: DiscoveryContract, publisher: TaskPublisher) -> None:
        self.contract = contract
        self.publisher = publisher
        self.shared_data = SharedDataHandler()

    def assign_host_to_client(self, did: str) -> str:
        return self.contract.get_user_queue(get_current_timestamp())

    def remove_host_from_client(self) -> None:
        pass

    def offload_to_queue(self, did: str, offload_request: OffloadRequest) -> str:
        queue = self.assign_host_to_client(did)
        if queue == "":
            return "Failed to assign host to client"

        # save correlation_id and origin_did of the message to match the result in result relayer
        correlation_id = str(uuid.uuid4())
        origin_did = offload_request.did
        self.shared_data.save_origin_did(correlation_id, origin_did)

        task_id = offload_request.task_id
        message = offload_request.content
        container_ref = offload_request.container_reference
        resource = offload_request.resource
        runtime = offload_request.runtime

        try:
            self.publisher.publish(correlation_id, task_id, message, container_ref, resource, runtime, host_name=queue)
        except Exception as e:
            return e
        
        return "Success"
