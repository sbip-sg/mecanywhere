from datetime import timedelta
import pika
from config import Config
from exceptions.http_exceptions import BadRequestException
from services.shared_data_handler import SharedDataHandler
import models.schema_pb2 as schema
import redis


class ResultQueue:
    _class_instance = None
    result_queue = "result_queue"

    def __init__(self, config: Config, cache: redis.Redis):
        self.config = config
        self.connection = None
        self.channel = None
        self.cache = cache
        self.shared_data = SharedDataHandler()

    def __new__(cls, config, cache):
        if cls._class_instance is None:
            cls._class_instance = super(ResultQueue, cls).__new__(cls)
        return cls._class_instance

    def stop(self):
        if self.channel is not None:
            print("Stopping consuming")
            self.channel.basic_cancel(consumer_tag=ResultQueue.result_queue)
            self.channel.stop_consuming()
            print("Stopped consuming")
        if self.connection is not None:
            print("Closing connection")
            self.connection.close()
            print("Connection closed")

    def start_consumer(self):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(self.config.get_mq_url())
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(
            queue=ResultQueue.result_queue,
            durable=True,
            arguments={"x-expires": 1000 * 60 * 30},
        )
        self.channel.basic_consume(
            queue=ResultQueue.result_queue,
            on_message_callback=self.callback,
            auto_ack=True,
        )
        print("Result relayer started consuming")
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        # Tests if the message is a TaskResult
        try:
            task = schema.TaskResult()
            task.ParseFromString(body)
            print(task, "received")
        except Exception as e:
            raise BadRequestException("Error parsing received result")

        correlation_id = properties.correlation_id
        origin_did = self.shared_data.get_origin_did(correlation_id)

        # drops the message when the origin_did is not found
        if origin_did is None:
            return

        self.shared_data.remove_origin_did(correlation_id)

        task_dict = {"id": task.id, "content": task.content}

        # TODO: handle error
        self.cache.hset(correlation_id, mapping=task_dict)
        self.cache.expire(correlation_id, timedelta(minutes=60 * 30))
