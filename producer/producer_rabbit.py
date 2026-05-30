import pika
from producer.transaction_event import TransactionEvent

QUEUE_NAME = "dinner_transactions_creeplyndarker"

RABBITMQ_HOST = "213.199.42.57"
RABBITMQ_PORT = 5672
RABBITMQ_VHOST = "/"
RABBITMQ_USER = "students"
RABBITMQ_PASSWORD = "Ut3c2026"

def create_connection():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)

    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        virtual_host=RABBITMQ_VHOST,
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
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        message = event.to_json()
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
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