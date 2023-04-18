import pika
import base64
import cloudpickle


class TaskConsumer:
    def compute(task):
        try:
            func = base64.b64decode(task)
            result = cloudpickle.loads(func)()
        except:
            result = ""
        finally:
            return result

    def on_request(ch, method, props, body):
        task = body

        print("Consuming task... : ", task)
        response = TaskConsumer.compute(task)
        print("Computed response : ", response)

        ch.basic_publish(
            exchange="",
            routing_key=props.reply_to,
            properties=pika.BasicProperties(
                correlation_id=props.correlation_id,
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                # content_type="application/json",
            ),
            body=response,
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def connect_and_consume(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )

        self.channel = self.connection.channel()
        self.channel.queue_declare(
            queue="consumer",
            durable=True,
        )
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue="consumer", on_message_callback=TaskConsumer.on_request
        )
        self.channel.start_consuming()

    def close(self):
        if self.connection:
            print("Closing connection...", self.connection)
            self.connection.close()
