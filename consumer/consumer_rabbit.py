import os
import pika
from dotenv import load_dotenv
from consumer.reward_processor import process_transaction_message

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


def callback(ch, method, properties, body) -> None:
    try:
        result = process_transaction_message(body.decode())

        print("\n[x] Transaction received")
        print(f"    Card: **** **** **** {result['card_last_digits']}")
        print(f"    Restaurant: {result['restaurant_code']}")
        print(f"    Amount: S/ {result['amount']:.2f}")
        print(f"    Date: {result['transaction_date']}")
        print(f"    Points earned: {result['points']}")
        print(f"    Cashback earned: S/ {result['cashback']:.2f}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as error:
        print(f"[!] Error processing message: {error}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def main() -> None:
    connection = None

    try:
        connection = create_connection()
        channel = connection.channel()

        queue_name = get_queue_name()
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_qos(prefetch_count=1)

        channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=False,
        )

        print(f'[*] Waiting for messages in queue "{queue_name}". Press CTRL+C to exit.')
        channel.start_consuming()

    except KeyboardInterrupt:
        print("\n[*] Consumer stopped by user.")

    finally:
        if connection is not None and connection.is_open:
            connection.close()
            print("[*] RabbitMQ connection closed.")

if __name__ == "__main__":
    main()