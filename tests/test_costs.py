import pytest

from us_ai_federalism.costs import estimate_cost


def test_batch_discount_is_half() -> None:
    regular = estimate_cost(["x" * 4000], "claude-haiku-4-5-20251001", 1000)
    batch = estimate_cost(["x" * 4000], "claude-haiku-4-5-20251001", 1000, batch=True)
    assert batch.usd == pytest.approx(regular.usd / 2)


def test_unknown_pricing_stops_spend() -> None:
    with pytest.raises(ValueError):
        estimate_cost(["text"], "unpriced-model")
