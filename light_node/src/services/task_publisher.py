import pika
import uuid


# Publishes tasks to RabbitMQ acting as a publisher client
class TaskPublisher(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(
            queue="",  # fresh queue
            exclusive=True,  # delete queue once connection is closed
            durable=True,
        )
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
        )

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def callRPC(self, n, exchange, routing_key):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        print("Publishing task to queue... : ", n)
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                # content_type="application/json",
            ),
            body=n,
        )
        self.connection.process_data_events(time_limit=None)
        return self.response
