#!/bin/python3

import os
import sys

import requests

IMDB_API_KEY = os.getenv("IMDB_API_KEY")


def searchMovie(query: str):
    response = requests.get(
        f"https://imdb-api.com/en/API/SearchMovie/{IMDB_API_KEY}/{query}"
    )
    results = response.json()["results"]

    for result in results:
        print(result)


if __name__ == "__main__":
    searchMovie(sys.argv[1])
