import json
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TransactionEvent:
    amount: float
    card_number: str
    restaurant_code: str
    transaction_date_time: str | None = None

    def to_json(self) -> str:
        event = {
            "eventType": "DinnerRegistered",
            "amount": self.amount,
            "cardNumber": self.card_number,
            "restaurantCode": self.restaurant_code,
            "transactionDateTime": self.transaction_date_time or datetime.now().isoformat(),
        }

        return json.dumps(event)