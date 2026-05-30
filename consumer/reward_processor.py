import json
from domain.reward_calculator import calculate_reward

def process_transaction_message(message_body: str) -> dict:
    transaction = json.loads(message_body)

    amount = float(transaction["amount"])
    card_number = transaction["cardNumber"]
    restaurant_code = transaction["restaurantCode"]
    transaction_date = transaction["transactionDateTime"]

    points, cashback = calculate_reward(amount, restaurant_code)

    return {
        "card_last_digits": card_number[-4:],
        "restaurant_code": restaurant_code,
        "amount": amount,
        "transaction_date": transaction_date,
        "points": points,
        "cashback": cashback,
    }