import json
from dataclasses import dataclass

@dataclass
class TransactionEvent:
    customer_id: str
    amount: float

    def to_json(self) -> str:
        return json.dumps({
            "customer_id": self.customer_id,
            "amount": self.amount
        })

    @staticmethod
    def from_json(message: str) -> "TransactionEvent":
        data = json.loads(message)

        return TransactionEvent(
            customer_id=data["customer_id"],
            amount=float(data["amount"])
        )
