import pika

from infrastructure.rabbitmq_connection import create_connection, get_queue_name
from producer.transaction_event import TransactionEvent


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