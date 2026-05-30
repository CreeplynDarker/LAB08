import os

import pika
from dotenv import load_dotenv
from producer.transaction_event import TransactionEvent

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
        username=os.getenv("RABBITMQ_USER", "students"),
        password=get_required_env("RABBITMQ_PASSWORD"),
    )

    parameters = pika.ConnectionParameters(
        host=os.getenv("RABBITMQ_HOST", "213.199.42.57"),
        port=int(os.getenv("RABBITMQ_PORT", "5672")),
        virtual_host=os.getenv("RABBITMQ_VHOST", "/"),
        credentials=credentials,
        connection_attempts=3,
        retry_delay=3,
        socket_timeout=10,
        blocked_connection_timeout=10,
        heartbeat=30,
    )

    return pika.BlockingConnection(parameters)


def send_transaction(event: TransactionEvent) -> None:
    connection = None

    try:
        connection = create_connection()
        channel = connection.channel()

        queue_name = get_queue_name()
        channel.queue_declare(queue=queue_name, durable=True)

        message = event.to_json()

        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(
                content_type="application/json",
                delivery_mode=2,
            ),
        )

        print("[x] Transaction sent successfully:")
        print(message)

    except pika.exceptions.AMQPConnectionError as error:
        print("[!] Could not connect to RabbitMQ.")
        print(error)

    finally:
        if connection is not None and connection.is_open:
            connection.close()

if __name__ == "__main__":
    transaction = TransactionEvent(
        amount=150.50,
        card_number="1234567890123456",
        restaurant_code="REST001",
    )

    send_transaction(transaction)