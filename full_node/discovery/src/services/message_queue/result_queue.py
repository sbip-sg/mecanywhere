import pika
from config import Config
from services.cache import DCache
import models.schema_pb2 as schema
from google.protobuf import json_format


class ResultQueue:
    _class_instance = None
    result_queue = "result_queue"

    def __init__(self, config: Config, cache: DCache):
        self.config = config
        self.connection = None
        self.channel = None
        self.cache = cache
        if not self.cache.ping():
            raise Exception("Cache is not running")

    def __new__(cls, config, cache):
        if cls._class_instance is None:
            cls._class_instance = super(ResultQueue, cls).__new__(cls)
        return cls._class_instance

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def stop(self):
        if self.channel is not None:
            print("Stopping consuming", flush=True)
            self.channel.basic_cancel(consumer_tag=ResultQueue.result_queue)
            self.channel.stop_consuming()
            print("Stopped consuming", flush=True)
        if self.connection is not None:
            print("Closing connection", flush=True)
            self.connection.close()
            print("Connection closed", flush=True)

    def start_consumer(self):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(
                self.config.get_mq_url()
                + "?heartbeat=300&blocked_connection_timeout=300"
            ),
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
        print("Result relayer started consuming", flush=True)
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        # Tests if the message is a TaskResult
        task_result = schema.TaskResult()
        try:
            task_result.ParseFromString(body)
            print(task_result, "received", flush=True)
        except Exception as e:
            print(e, "error parsing received result", flush=True)
            task_result.content = str(e)

        transaction_id = properties.correlation_id
        task_result_json = json_format.MessageToJson(
            task_result, preserving_proto_field_name=True
        )

        try:
            hostdid = self.cache.get_recipient(transaction_id)
        except Exception as e:
            print(e, "error getting publish receipt", flush=True)
        if hostdid is None:
            print(
                f"Host for published transaction {transaction_id} not found in cache",
                flush=True,
            )
        else:
            self.cache.delete_recipient(transaction_id)

        self.cache.set_result(transaction_id, task_result_json)
        