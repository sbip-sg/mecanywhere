import pika
from config import Config
import models.schema_pb2 as schema
from services.result_relayer import ResultRelayer


class TaskPublisher:
    _class_instance = None
    openQueues = {}

    def __init__(self, config: Config):
        self.config = config
        self.connection = None
        self.channel = None
        self.start_publisher()

    def __new__(cls, config):
        if cls._class_instance is None:
            cls._class_instance = super(TaskPublisher, cls).__new__(cls)
        return cls._class_instance

    def start_publisher(self):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(self.config.get_mq_url())
        )
        self.channel = self.connection.channel()
        print("Task publisher started")

    def publish(self, correlation_id, message, container_ref, host_name):
        task = schema.Task()
        task.id = correlation_id
        task.containerRef = container_ref
        task.content = message

        self.channel.queue_declare(
            queue=host_name, durable=True, arguments={"x-expires": 1000 * 60 * 30}
        )
        self.channel.basic_publish(
            exchange="",
            routing_key=host_name,
            properties=pika.BasicProperties(
                correlation_id=correlation_id,
                reply_to=ResultRelayer.result_queue,
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
            ),
            body=task.SerializeToString(),
        )

    def close(self):
        self.connection.close()
