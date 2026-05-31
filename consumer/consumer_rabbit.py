from consumer.reward_processor import process_transaction_message
from infrastructure.rabbitmq_connection import create_connection, get_queue_name

def callback(ch, method, _properties, body) -> None:
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