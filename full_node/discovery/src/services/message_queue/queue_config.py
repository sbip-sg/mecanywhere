import pika


def declare_rpc_queue(channel: pika.channel.Channel):
    return channel.queue_declare(
        queue="", exclusive=True, durable=True, auto_delete=True
    )


def declare_host_queue(channel: pika.channel.Channel, host_name: str):
    try:
        return channel.queue_declare(
            queue=host_name, durable=True, auto_delete=True, passive=True
        )
    except pika.exceptions.ChannelClosedByBroker as e:
        print(f"Channel closed by broker. {e}")
        raise e
    except pika.exceptions.StreamLostError as e:
        print(f"Stream lost. {e}")
        raise e
