import pika
import json
import sys
import os

credenciales = pika.PlainCredentials("students", "Ut3c2026")
parametros = pika.ConnectionParameters(
    host="213.199.42.57",
    port=5672,
    virtual_host="/",
    credentials=credenciales
)

QUEUE_NAME = "dinner_transactions"

def calculate_reward(amount, restaurant_code):
    points = int(amount)
    cashback = amount * 0.05

    if restaurant_code == "REST001":
        points += int(points * 0.10)

    return points, cashback

def callback(ch, method, properties, body):
    try:
        transaction = json.loads(body.decode())

        amount = float(transaction["amount"])
        card_number = transaction["cardNumber"]
        restaurant_code = transaction["restaurantCode"]
        transaction_date = transaction["transactionDateTime"]

        points, cashback = calculate_reward(amount, restaurant_code)

        print("\n [x] Transaction received")
        print(f"     Card: **** **** **** {card_number[-4:]}")
        print(f"     Restaurant: {restaurant_code}")
        print(f"     Amount: S/ {amount:.2f}")
        print(f"     Date: {transaction_date}")
        print(f"     Points earned: {points}")
        print(f"     Cashback earned: S/ {cashback:.2f}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as error:
        print(f" [!] Error processing message: {error}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def main():
    conexion = None

    try:
        conexion = pika.BlockingConnection(parametros)
        canal = conexion.channel()

        canal.queue_declare(queue=QUEUE_NAME, durable=True)
        canal.basic_qos(prefetch_count=1)

        canal.basic_consume(
            queue=QUEUE_NAME,
            on_message_callback=callback,
            auto_ack=False
        )

        print(f' [*] Waiting for messages in queue "{QUEUE_NAME}". Press CTRL+C to exit.')
        canal.start_consuming()

    except KeyboardInterrupt:
        print("\n [*] Consumer stopped by user.")

    finally:
        if conexion is not None and conexion.is_open:
            conexion.close()
            print(" [*] RabbitMQ connection closed.")

if __name__ == "__main__":
    main()