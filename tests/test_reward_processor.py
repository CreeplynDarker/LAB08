import json
import pytest
from consumer.reward_processor import process_transaction_message

def test_process_transaction_message_normal_restaurant():
    message = json.dumps({
        "eventType": "DinnerRegistered",
        "amount": 100.0,
        "cardNumber": "1234567890123456",
        "restaurantCode": "REST002",
        "transactionDateTime": "2026-05-28T21:17:26"
    })

    result = process_transaction_message(message)

    assert result["card_last_digits"] == "3456"
    assert result["restaurant_code"] == "REST002"
    assert result["amount"] == 100.0
    assert result["points"] == 100
    assert result["cashback"] == 5.0

def test_process_transaction_message_bonus_restaurant():
    message = json.dumps({
        "eventType": "DinnerRegistered",
        "amount": 100.0,
        "cardNumber": "1234567890123456",
        "restaurantCode": "REST001",
        "transactionDateTime": "2026-05-28T21:17:26"
    })

    result = process_transaction_message(message)

    assert result["points"] == 110
    assert result["cashback"] == 5.0

def test_process_transaction_message_invalid_json():
    with pytest.raises(json.JSONDecodeError):
        process_transaction_message("not valid json")

def test_process_transaction_message_invalid_amount():
    message = json.dumps({
        "eventType": "DinnerRegistered",
        "amount": -50.0,
        "cardNumber": "1234567890123456",
        "restaurantCode": "REST001",
        "transactionDateTime": "2026-05-28T21:17:26"
    })

    with pytest.raises(ValueError):
        process_transaction_message(message)