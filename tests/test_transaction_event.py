import json
from producer.transaction_event import TransactionEvent

def test_transaction_event_to_json():
    event = TransactionEvent(
        amount=100.0,
        card_number="1234567890123456",
        restaurant_code="REST001",
        transaction_date_time="2026-05-30T14:16:33"
    )
    json_message = event.to_json()
    data = json.loads(json_message)
    assert data["eventType"] == "DinnerRegistered"
    assert data["amount"] == 100.0
    assert data["cardNumber"] == "1234567890123456"
    assert data["restaurantCode"] == "REST001"
    assert data["transactionDateTime"] == "2026-05-30T14:16:33"


def test_transaction_event_from_json():
    message = json.dumps({
        "eventType": "DinnerRegistered",
        "amount": 100.0,
        "cardNumber": "1234567890123456",
        "restaurantCode": "REST001",
        "transactionDateTime": "2026-05-30T14:16:33"
    })
    event = TransactionEvent.from_json(message)
    assert event.amount == 100.0
    assert event.card_number == "1234567890123456"
    assert event.restaurant_code == "REST001"
    assert event.transaction_date_time == "2026-05-30T14:16:33"


def test_transaction_event_round_trip():
    original_event = TransactionEvent(
        amount=250.5,
        card_number="9876543210987654",
        restaurant_code="REST002",
        transaction_date_time="2026-05-30T15:00:00"
    )
    json_message = original_event.to_json()
    recovered_event = TransactionEvent.from_json(json_message)
    assert recovered_event.amount == original_event.amount
    assert recovered_event.card_number == original_event.card_number
    assert recovered_event.restaurant_code == original_event.restaurant_code
    assert recovered_event.transaction_date_time == original_event.transaction_date_time