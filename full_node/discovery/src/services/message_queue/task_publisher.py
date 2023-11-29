import threading
from time import sleep
import pika
from config import Config
from services.message_queue.queue_config import declare_rpc_queue, declare_host_queue
from models.responses import TaskResultModel
from models.requests import OffloadRequest
import models.schema_pb2 as schema
from services.message_queue.result_queue import ResultQueue
from google.protobuf import json_format


class RPCTaskPublisher:
    _class_instance = None
    openQueues = {}
    internal_lock = threading.Lock()
    responses_lock = threading.Lock()
    responses = dict()

    def __init__(self, config: Config):
        self.config = config
        self.connection = None
        self.channel = None
        self.rpc_queue = ""
        self.start_publisher()

    def __new__(cls, config):
        if cls._class_instance is None:
            cls._class_instance = super(RPCTaskPublisher, cls).__new__(cls)
        return cls._class_instance

    def start_publisher(self):
        connection_params = pika.URLParameters(self.config.get_mq_url())
        connection_params.blocked_connection_timeout = 60
        self.connection = pika.BlockingConnection(connection_params)

        self.channel = self.connection.channel()
        self.channel.confirm_delivery()
        self.rpc_queue = declare_rpc_queue(self.channel).method.queue

        self.processing_thread = threading.Thread(target=self._process_data_events)
        self.processing_thread.setDaemon(True)
        self.processing_thread.start()
        print("Task publisher started")

    def _process_data_events(self):
        self.channel.basic_consume(
            queue=self.rpc_queue,
            on_message_callback=self.on_response,
            auto_ack=False,
        )
        while True:
            with self.internal_lock:
                self.connection.process_data_events()
            sleep(0.1)

    def on_response(self, ch, method, props, body):
        task_result = schema.TaskResult()
        try:
            task_result.ParseFromString(body)
            print(task_result, "received")
        except Exception as e:
            print(e, "error parsing received result")
            task_result.content = str(e)
        task_result_dict = json_format.MessageToDict(
            task_result, preserving_proto_field_name=True
        )
        with self.responses_lock:
            self.responses[props.correlation_id] = TaskResultModel(**task_result_dict)
        print("task_publisher response")
        print(task_result_dict)

    async def publish(
        self,
        transaction_id: str,
        offload_request: OffloadRequest,
        host_name: str,
        reply_to: str = None,
    ) -> TaskResultModel:
        task = schema.Task()
        task.id = offload_request.task_id
        task.containerRef = offload_request.container_reference
        task.content = offload_request.content
        if offload_request.resource is not None:
            task.resource.update(offload_request.resource)
        if offload_request.runtime is not None:
            task.runtime = offload_request.runtime

        declare_host_queue(self.channel, host_name)
        print("Publishing to queue: " + host_name)
        print(task)
        if reply_to is None:
            reply_to = self.rpc_queue
        self.channel.basic_publish(
            exchange="",
            routing_key=host_name,
            properties=pika.BasicProperties(
                correlation_id=transaction_id,
                reply_to=reply_to,
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
            ),
            body=task.SerializeToString(),
            mandatory=True,
        )
        return TaskResultModel(
            id=task.id,
            content=transaction_id,
        )

    def get_response(self, transaction_id: str) -> TaskResultModel:
        with self.responses_lock:
            if transaction_id not in self.responses:
                return None
            response = self.responses[transaction_id]
            del self.responses[transaction_id]
            return response

    def close(self):
        with self.internal_lock:
            self.channel.stop_consuming()
            self.processing_thread.join()
            self.connection.close()
