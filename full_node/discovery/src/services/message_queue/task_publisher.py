import threading
import pika
from config import Config
from models.requests import OffloadRequest
import models.schema_pb2 as schema
from services.message_queue.result_queue import ResultQueue


class RPCTaskPublisher:
    _class_instance = None
    openQueues = {}

    def __init__(self, config: Config):
        self.config = config
        self.connection = None
        self.channel = None
        self.synchronous_queue = ""
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
        self.synchronous_queue = self.channel.queue_declare(
            queue="", exclusive=True, durable=True, auto_delete=True
        ).method.queue

        self.channel.basic_consume(
            queue=self.synchronous_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
        )
        print("Task publisher started")

    def on_response(self, ch, method, props, body):
        response = None
        try:
            task = schema.TaskResult()
            task.ParseFromString(body)
            print(task, "received")
            response = task.content
        except Exception as e:
            print(e, "error parsing received result")
            response = str(e)
        with self.responses_lock:
            self.responses[props.correlation_id] = response

    async def publish(
        self, correlation_id: str, offload_request: OffloadRequest, host_name: str
    ):
        task = schema.Task()
        task.id = offload_request.task_id
        task.containerRef = offload_request.container_reference
        task.content = offload_request.content
        if offload_request.resource is not None:
            task.resource.update(offload_request.resource)
        if offload_request.runtime is not None:
            task.runtime = offload_request.runtime

        # TODO: centralize queue definition and declaration
        self.channel.queue_declare(
            queue=host_name, durable=True, arguments={"x-expires": 1000 * 60 * 30}
        )
        self.channel.basic_publish(
            exchange="",
            routing_key=host_name,
            properties=pika.BasicProperties(
                correlation_id=correlation_id,
                reply_to=self.synchronous_queue,
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
    ):
        task = schema.Task()
        task.id = offload_request.task_id
        task.containerRef = offload_request.container_reference
        task.content = offload_request.content
        if offload_request.resource is not None:
            task.resource.update(offload_request.resource)
        if offload_request.runtime is not None:
            task.runtime = offload_request.runtime

        self.channel.queue_declare(
            queue=host_name, durable=True, arguments={"x-expires": 1000 * 60 * 30}
        )
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
        return correlation_id

    def close(self):
        self.connection.close()
