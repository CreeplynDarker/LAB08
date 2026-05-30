import pika
from producer.transaction_event import TransactionEvent

QUEUE_NAME = "transaction_queue"

def send_transaction(event: TransactionEvent) -> None:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    message = event.to_json()
    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=message
    )
    print(f"Sent transaction: {message}")
    connection.close()

if __name__ == "__main__":
    transaction = TransactionEvent(
        customer_id="C001",
        amount=100.0
    )
    send_transaction(transaction)