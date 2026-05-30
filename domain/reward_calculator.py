def calculate_reward(amount: float, restaurant_code: str) -> tuple[int, float]:
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")

    points = int(amount)
    cashback = amount * 0.05

    if restaurant_code == "REST001":
        points += int(points * 0.10)

    return points, cashback