import pytest
from domain.reward_calculator import calculate_reward

def test_calculate_reward_normal_restaurant():
    points, cashback = calculate_reward(100.0, "REST002")
    assert points == 100
    assert cashback == 5.0

def test_calculate_reward_bonus_restaurant():
    points, cashback = calculate_reward(100.0, "REST001")
    assert points == 110
    assert cashback == 5.0

def test_calculate_reward_invalid_amount():
    with pytest.raises(ValueError):
        calculate_reward(-50.0, "REST001")