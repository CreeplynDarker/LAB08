from domain.reward_calculator import calculate_reward

def test_calculate_reward_normal_amount():
    assert calculate_reward(100) == 10

def test_calculate_reward_decimal_amount():
    assert calculate_reward(95.50) == 9

def test_calculate_reward_zero():
    assert calculate_reward(0) == 0

def test_calculate_reward_negative_amount():
    try:
        calculate_reward(-50)
        assert False
    except ValueError:
        assert True