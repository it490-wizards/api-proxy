# api-proxy

This repository is a backend component for interfacing with the [IMDb API](https://imdb-api.com/).

## Installation

```sh
python3 -m pip install -r requirements.txt
```

Create a file `.env` which defines the necessary environment variables.

```sh
IMDB_API_KEY=...
PIKA_HOST="localhost"
PIKA_PORT=5672
PIKA_USER="guest"
PIKA_PASSWORD="guest"
PIKA_VHOST="/"
```
