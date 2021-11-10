import os

import dotenv
import requests

dotenv.load_dotenv()

IMDB_API_KEY = os.getenv("IMDB_API_KEY")


def search_movie(query: str) -> list:
    response = requests.get(
        f"https://imdb-api.com/en/API/SearchMovie/{IMDB_API_KEY}/{query}"
    )
    if response:
        result = response.json()
        return result.get("results") or []
    else:
        return []


def title(imdb_id: str) -> dict:
    # which data to extract from API result
    keyFilter = [
        "id",
        "title",
        "year",
        "releaseDate",
        "runtimeMins",
        "image",
        "languages",
        "genres",
    ]

    response = requests.get(
        f"https://imdb-api.com/en/API/Title/{IMDB_API_KEY}/{imdb_id}"
    )
    if response:
        result = response.json()
        return {key: result[key] for key in keyFilter}
    else:
        return {}


def get_top10() -> list:
    response = requests.get(f"https://imdb-api.com/en/API/Top250Movies/{IMDB_API_KEY}")
    result = response.json()

    return [title(item["id"]) for item in result["items"][:10]]
