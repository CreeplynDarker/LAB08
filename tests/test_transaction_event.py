from producer.transaction_event import TransactionEvent

def test_transaction_event_to_json():
    event = TransactionEvent(customer_id="C001", amount=100.0)

    json_message = event.to_json()

    assert '"customer_id": "C001"' in json_message
    assert '"amount": 100.0' in json_message

def test_transaction_event_from_json():
    message = '{"customer_id": "C001", "amount": 100.0}'

    event = TransactionEvent.from_json(message)

    assert event.customer_id == "C001"
    assert event.amount == 100.0

def test_transaction_event_round_trip():
    original_event = TransactionEvent(customer_id="C002", amount=250.5)

    json_message = original_event.to_json()
    recovered_event = TransactionEvent.from_json(json_message)

    assert recovered_event.customer_id == original_event.customer_id
    assert recovered_event.amount == original_event.amount