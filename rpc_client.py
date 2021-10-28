#!/usr/bin/env python

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

    def call(self, s: str) -> str:
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange="",
            routing_key="rpc_queue",
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=s.encode(),
        )
        while self.response is None:
            self.connection.process_data_events()
        return self.response


if __name__ == "__main__":
    movieinfo_rpc = MovieInfoRpcClient()
    response = movieinfo_rpc.call(sys.argv[1])
    print(response)
