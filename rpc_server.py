#!/usr/bin/env python3

import json
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
    connection = pika.BlockingConnection()

    channel = connection.channel()
    channel.queue_declare(queue="rpc_queue")
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue="rpc_queue",
        on_message_callback=on_request,
    )
    channel.start_consuming()


if __name__ == "__main__":
    main()
