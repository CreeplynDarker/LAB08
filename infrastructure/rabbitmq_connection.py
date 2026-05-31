import os

import pika
from dotenv import load_dotenv

load_dotenv()

def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")

    return value

def get_queue_name() -> str:
    return os.getenv("RABBITMQ_QUEUE", "dinner_transactions_creeplyndarker")

def create_connection() -> pika.BlockingConnection:
    credentials = pika.PlainCredentials(
        username=get_required_env("RABBITMQ_USER"),
        password=get_required_env("RABBITMQ_PASSWORD"),
    )

    parameters = pika.ConnectionParameters(
        host=get_required_env("RABBITMQ_HOST"),
        port=int(get_required_env("RABBITMQ_PORT")),
        virtual_host=get_required_env("RABBITMQ_VHOST"),
        credentials=credentials,
        connection_attempts=3,
        retry_delay=3,
        socket_timeout=10,
        blocked_connection_timeout=10,
        heartbeat=30,
    )

    return pika.BlockingConnection(parameters)