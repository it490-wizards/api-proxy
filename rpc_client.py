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

    def call(self, request: str) -> str:
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
        return self.response

    def search_movie(self, query: str) -> list:
        response = self.call(
            json.dumps(
                {
                    "func": "search_movie",
                    "params": [query],
                }
            )
        )
        return json.loads(response)

    def title(self, imdb_id: str) -> dict:
        response = self.call(
            json.dumps(
                {
                    "func": "title",
                    "params": [imdb_id],
                }
            )
        )
        return json.loads(response)


def main():
    client = MovieInfoRpcClient()
    print(client.search_movie(sys.argv[1]))


if __name__ == "__main__":
    main()
