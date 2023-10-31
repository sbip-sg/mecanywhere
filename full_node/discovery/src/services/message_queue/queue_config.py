import pika


def declare_rpc_queue(channel: pika.channel.Channel):
    return channel.queue_declare(
        queue="", exclusive=True, durable=True, auto_delete=True
    )


def declare_host_queue(channel: pika.channel.Channel, host_name: str):
    return channel.queue_declare(
        queue=host_name, durable=True, arguments={"x-expires": 1000 * 60 * 30}
    )
