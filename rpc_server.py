#!/usr/bin/env python

import json
import time

import pika

import search


def on_request(ch, method, props, body: bytes):
    s = body.decode()
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    print(f"[{ts}] {s}")

    response = json.dumps(search.search_movie(s))

    ch.basic_publish(
        exchange="",
        routing_key=props.reply_to,
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id,
        ),
        body=str(response),
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


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
