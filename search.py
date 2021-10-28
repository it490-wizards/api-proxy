#!/bin/python3

import os
import sys

import dotenv
import requests

dotenv.load_dotenv()

IMDB_API_KEY = os.getenv("IMDB_API_KEY")


def searchMovie(query: str) -> list:
    response = requests.get(
        f"https://imdb-api.com/en/API/SearchMovie/{IMDB_API_KEY}/{query}"
    )
    result = response.json()

    return result["results"]


def getTitle(imdb_id: str) -> dict:
    # which data to extract from API result
    keyFilter = [
        "id",
        "title",
        "year",
        "releaseDate",
        "runtimeMins",
        "image",
        "genreList",
    ]

    response = requests.get(
        f"https://imdb-api.com/en/API/Title/{IMDB_API_KEY}/{imdb_id}"
    )
    result = response.json()

    return {key: result[key] for key in keyFilter}


if __name__ == "__main__":
    if IMDB_API_KEY is None:
        print("'IMDB_API_KEY' not set", file=sys.stderr)
        exit(1)

    # TODO: temporary
    titles = searchMovie(sys.argv[1])
    print(getTitle(titles[0]["id"]))
