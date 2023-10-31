import threading
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

    def __init__(self, config: Config):
        self.config = config
        self.connection = None
        self.channel = None
        self.rpc_queue = ""
        self.responses = dict()
        self.responses_lock = threading.Lock()
        self.start_publisher()

    def __new__(cls, config):
        if cls._class_instance is None:
            cls._class_instance = super(RPCTaskPublisher, cls).__new__(cls)
        return cls._class_instance

    def start_publisher(self):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(self.config.get_mq_url())
        )
        self.channel = self.connection.channel()
        self.rpc_queue = declare_rpc_queue(self.channel).method.queue

        self.channel.basic_consume(
            queue=self.rpc_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
        )
        print("Task publisher started")

    def on_response(self, ch, method, props, body):
        task_result = schema.TaskResult()
        try:
            task_result.ParseFromString(body)
            print(task_result, "received")
        except Exception as e:
            print(e, "error parsing received result")
            task_result.content = str(e)
        task_result_dict = json_format.MessageToDict(task_result, preserving_proto_field_name=True)
        with self.responses_lock:
            self.responses[props.correlation_id] = TaskResultModel(**task_result_dict)
        print("task_publisher response")
        print(task_result_dict)

    async def publish(
        self, correlation_id: str, offload_request: OffloadRequest, host_name: str
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
        self.channel.basic_publish(
            exchange="",
            routing_key=host_name,
            properties=pika.BasicProperties(
                correlation_id=correlation_id,
                reply_to=self.rpc_queue,
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
            ),
            body=task.SerializeToString(),
        )
        self.connection.process_data_events(time_limit=None)
        result = None
        with self.responses_lock:
            result = self.responses[correlation_id]
            del self.responses[correlation_id]
        return result

    def close(self):
        self.connection.close()


class BasicTaskPublisher:
    _class_instance = None
    openQueues = {}

    def __init__(self, config: Config):
        self.config = config
        self.connection = None
        self.channel = None
        self.start_publisher()

    def __new__(cls, config):
        if cls._class_instance is None:
            cls._class_instance = super(BasicTaskPublisher, cls).__new__(cls)
        return cls._class_instance

    def start_publisher(self):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(self.config.get_mq_url())
        )
        self.channel = self.connection.channel()
        print("Basic task publisher started")

    async def publish(
        self, correlation_id: str, offload_request: OffloadRequest, host_name: str
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
        self.channel.basic_publish(
            exchange="",
            routing_key=host_name,
            properties=pika.BasicProperties(
                correlation_id=correlation_id,
                reply_to=ResultQueue.result_queue,
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
            ),
            body=task.SerializeToString(),
        )
        return TaskResultModel(
            id=task.id,
            resource_consumed=0,
            transaction_start_datetime=0,
            transaction_end_datetime=0,
            content=correlation_id,
            duration=0,
        )

    def close(self):
        self.connection.close()
