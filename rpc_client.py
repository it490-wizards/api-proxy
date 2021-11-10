#!/usr/bin/env python3

import json
import sys
import uuid

import pika


class MovieInfoRpcClient:
    def __init__(self):
        self.connection = pika.BlockingConnection()

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(
            queue="",
            exclusive=True,
        )
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
        )

    def on_response(self, ch, method, props, body: bytes):
        if self.corr_id == props.correlation_id:
            self.response = body.decode()

    def call(self, func: str, *args) -> str:
        request = json.dumps({"func": func, "args": args})
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange="",
            routing_key="rpc_queue",
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=request.encode(),
        )
        while self.response is None:
            self.connection.process_data_events()

        return json.loads(self.response)


def main():
    client = MovieInfoRpcClient()
    print(client.call("search_movie", sys.argv[1]))


if __name__ == "__main__":
    main()
