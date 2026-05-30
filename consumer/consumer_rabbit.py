import os
import sys
import pika
from consumer.reward_processor import process_transaction_message

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


def callback(ch, method, properties, body):
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


def main():
    connection = None

    try:
        connection = create_connection()
        channel = connection.channel()

        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        channel.basic_qos(prefetch_count=1)

        channel.basic_consume(
            queue=QUEUE_NAME,
            on_message_callback=callback,
            auto_ack=False,
        )

        print(f'[*] Waiting for messages in queue "{QUEUE_NAME}". Press CTRL+C to exit.')
        channel.start_consuming()

    except KeyboardInterrupt:
        print("\n[*] Consumer stopped by user.")

    finally:
        if connection is not None and connection.is_open:
            connection.close()
            print("[*] RabbitMQ connection closed.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Exiting consumer...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)