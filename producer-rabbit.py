import pika
import json
from datetime import datetime

credenciales = pika.PlainCredentials("students", "Ut3c2026")
parametros = pika.ConnectionParameters(
    host="213.199.42.57",
    port=5672,
    virtual_host="/",
    credentials=credenciales
)

QUEUE_NAME = "dinner_transactions"

def main():
    conexion = pika.BlockingConnection(parametros)
    canal = conexion.channel()

    canal.queue_declare(queue=QUEUE_NAME, durable=True)

    transaction_event = {
        "eventType": "DinnerRegistered",
        "amount": 150.50,
        "cardNumber": "1234567890123456",
        "restaurantCode": "REST001",
        "transactionDateTime": datetime.now().isoformat()
    }

    message = json.dumps(transaction_event)

    canal.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=message,
        properties=pika.BasicProperties(
            content_type="application/json",
            delivery_mode=2
        )
    )

    print(f" [x] Dinner transaction sent: {message}")

    conexion.close()

if __name__ == "__main__":
    main()