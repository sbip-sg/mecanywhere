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

def declare_result_queue(channel: pika.channel.Channel, result_queue: str):
    return channel.queue_declare(
        queue=result_queue, 
        durable=True,
        arguments={"x-expires": 1000 * 60 * 30},
    )
