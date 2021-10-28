#!/usr/bin/env python

import json
import time

import pika
from pika.spec import Basic, BasicProperties, Channel

import search


def on_request(
    channel: Channel, method: Basic.Deliver, properties: BasicProperties, body: bytes
):
    request = body.decode()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    print(f"[{timestamp}] {request}")

    response = json.dumps(search.search_movie(request))

    channel.basic_publish(
        exchange="",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id,
        ),
        body=str(response),
    )
    channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    connection = pika.BlockingConnection()

    channel = connection.channel()
    channel.queue_declare(queue="rpc_queue")
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue="rpc_queue",
        on_message_callback=on_request,
    )
    channel.start_consuming()
