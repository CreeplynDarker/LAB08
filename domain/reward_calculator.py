def calculate_reward(amount: float) -> int:
    """
    Calculates reward points from a transaction amount.

    Rule:
    1 reward point for every 10 monetary units.
    Example:
    amount = 100 -> 10 points
    """

    if amount < 0:
        raise ValueError("Amount cannot be negative")

    return int(amount // 10)