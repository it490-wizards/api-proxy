#!/usr/bin/env python3

import json
import os
import time

import pika

import search


def on_request(ch, method, properties, body: bytes):
    # log request with timestamp
    request = body.decode()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    print(f"[{timestamp}] {request}")

    # unpack the function and parameters from request
    request_obj = json.loads(request)
    func = request_obj.get("func")
    args = request_obj.get("args")
    if func == "search_movie":
        response = search.search_movie(*args)
    elif func == "title":
        response = search.title(*args)
    else:
        response = None

    ch.basic_publish(
        exchange="",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id,
        ),
        body=json.dumps(response).encode(),
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.getenv("PIKA_HOST"),
            port=int(os.getenv("PIKA_PORT")),
            virtual_host=os.getenv("PIKA_VHOST"),
            credentials=pika.PlainCredentials(
                username=os.getenv("PIKA_USER"),
                password=os.getenv("PIKA_PASSWORD"),
            ),
        )
    )

    channel = connection.channel()
    channel.queue_declare(queue="rpc_queue")
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue="rpc_queue",
        on_message_callback=on_request,
    )
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
